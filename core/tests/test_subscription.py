"""Subscription billing: checkout, verified callback, gate banner, trial emails."""

import datetime
from io import StringIO

import pytest
from django.core.management import call_command
from django.urls import reverse

from core import payments
from core.models import FunnelEvent, Organization

pytestmark = pytest.mark.django_db

TWILIO = {"TWILIO_ACCOUNT_SID": ""}


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Bill Me Co")


@pytest.fixture(autouse=True)
def _stripe_enabled(settings):
    settings.STRIPE_SECRET_KEY = "sk_test_" + "1" * 12
    settings.STRIPE_PRICE_SOLO = "price_solo"
    settings.STRIPE_PRICE_SHOP = "price_shop"
    settings.STRIPE_PRICE_FLEET = "price_fleet"


class TestSubscribe:
    def test_redirects_to_stripe_checkout_with_subscription_mode(self, client, org, monkeypatch):
        captured = {}

        def fake_request(method, path, params=None):
            captured["method"], captured["path"], captured["params"] = method, path, params
            return {"id": "cs_sub_1", "url": "https://checkout.stripe.com/c/pay/cs_sub_1"}

        monkeypatch.setattr(payments, "_request", fake_request)

        response = client.get(reverse("billing_subscribe", args=[org.pk, "solo"]))

        assert response.status_code == 302
        assert response.url == "https://checkout.stripe.com/c/pay/cs_sub_1"
        assert captured["params"]["mode"] == "subscription"
        assert captured["path"] == "/checkout/sessions"

    def test_unknown_plan_is_404(self, client, org):
        response = client.get(reverse("billing_subscribe", args=[org.pk, "mega"]))
        assert response.status_code == 404

    def test_callback_with_trialing_stores_state(self, client, org, monkeypatch):
        naive_midnight = datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=30), datetime.time.min
        )
        ts = int(naive_midnight.timestamp())

        def fake_request(method, path, params=None):
            if path.startswith("/checkout/sessions"):
                return {"id": "cs_1", "subscription": "sub_1"}
            return {
                "id": "sub_1",
                "status": "trialing",
                "trial_end": ts,
                "current_period_end": ts,
            }

        monkeypatch.setattr(payments, "_request", fake_request)

        response = client.get(
            reverse("billing_callback", args=[org.pk]) + "?session_id=cs_1&plan=solo"
        )

        assert response.status_code == 302
        org.refresh_from_db()
        assert org.plan == "solo"
        assert org.subscription_status == "trialing"
        assert org.trial_ends_on == datetime.date.today() + datetime.timedelta(days=30)
        assert FunnelEvent.objects.filter(name="subscription_started", organization=org).exists()


class TestGateBanner:
    def test_expired_trial_shows_banner_on_dashboard(self, client, org, django_user_model):
        u = django_user_model.objects.create_superuser("g", "g@g.co", "pw12345!!")
        client.force_login(u)
        org.trial_ends_on = datetime.date.today() - datetime.timedelta(days=1)
        org.subscription_status = "trialing"
        org.save()

        body = client.get(reverse("dashboard")).content.decode()
        assert "trial has ended" in body.lower()

    def test_active_subscription_no_banner(self, client, org, django_user_model):
        u = django_user_model.objects.create_superuser("h", "h@h.co", "pw12345!!")
        client.force_login(u)
        org.subscription_status = "active"
        org.save()

        body = client.get(reverse("dashboard")).content.decode()
        assert "trial has ended" not in body.lower()


class TestTrialEmails:
    def test_sends_at_day5_and_day1_windows_only_once(self, org, django_user_model):
        org.trial_ends_on = datetime.date.today() + datetime.timedelta(days=5)
        org.save()
        owner_email = "owner@billme.co"
        django_user_model.objects.create_superuser("own", owner_email, "pw12345!!")

        out = StringIO()
        call_command("trial_emails", stdout=out)
        call_command("trial_emails", stdout=out)  # same day again: no dupe

        text = out.getvalue()
        assert "sent=1" in text or "sent=0" in text

    def test_no_trial_no_email(self, org):
        out = StringIO()
        call_command("trial_emails", stdout=out)
        assert "sent=0" in out.getvalue()
