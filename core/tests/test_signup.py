"""Self-serve signup and public pricing page tests."""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.marketing_data import PLANS
from core.models import Organization

pytestmark = pytest.mark.django_db


def _payload(**overrides: str) -> dict[str, str]:
    base = {
        "shop_name": "Valley Septic",
        "email": "owner@valley.test",
        "password1": "Qwerty!23456",
        "password2": "Qwerty!23456",
        "website": "",
    }
    base.update(overrides)
    return base


class TestSignup:
    def test_get_renders_for_anonymous(self):
        response = Client().get(reverse("signup"))
        assert response.status_code == 200

    def test_post_creates_org_user_and_logs_in(self):
        response = Client().post(reverse("signup"), _payload())

        assert response.status_code == 302
        assert response.url == reverse("dashboard")
        Organization.objects.get(name="Valley Septic")
        created = User.objects.get(username="owner@valley.test")
        assert created.check_password("Qwerty!23456")
        assert Organization.objects.get(name="Valley Septic").customers.count() == 0

    def test_duplicate_email_rejected(self):
        client = Client()
        client.post(reverse("signup"), _payload())

        second = Client().post(reverse("signup"), _payload(shop_name="Second Septic"))

        assert second.status_code == 200
        assert Organization.objects.filter(name="Second Septic").count() == 0

    def test_honeypot_rejects_bots(self):
        response = Client().post(reverse("signup"), _payload(website="http://spam.tld"))

        assert response.status_code == 302
        assert Organization.objects.count() == 0

    def test_password_mismatch_rejected(self):
        response = Client().post(reverse("signup"), _payload(password2="Different!234"))

        assert response.status_code == 200
        assert b"do not match" in response.content.lower()

    def test_weak_password_rejected(self):
        response = Client().post(reverse("signup"), _payload(password1="123", password2="123"))

        assert response.status_code == 200
        assert Organization.objects.count() == 0


class TestPricingPage:
    def test_public_page_lists_both_plans(self):
        response = Client().get(reverse("pricing"))

        assert response.status_code == 200
        body = response.content.decode()
        for plan in PLANS:
            assert plan["price"] in body
            assert plan["name"] in body

    def test_pricing_in_sitemap(self):
        response = Client().get("/sitemap.xml")

        assert b"/pricing/" in response.content
