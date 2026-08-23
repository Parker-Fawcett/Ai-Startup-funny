"""Stripe bridge tests — transport is mocked, nothing leaves the machine."""

import datetime
from decimal import Decimal

import pytest
from django.test import Client
from django.urls import reverse

from core import payments
from core.billing_models import Invoice, PaymentMethod
from core.models import Customer, Job, Organization

pytestmark = pytest.mark.django_db


@pytest.fixture
def org():
    return Organization.objects.create(name="Card Shop")


@pytest.fixture
def client(client: Client, user):
    return client


def _due_invoice(org) -> Invoice:
    customer = Customer.objects.create(
        organization=org,
        name="Card Buyer",
        address="1 Rd",
        tank_size_gallons=1000,
        email="buyer@card.test",
    )
    job = Job.objects.create(organization=org, customer=customer, route_day=datetime.date.today())
    job.mark_completed(
        gallons=1350, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
    )
    return job.invoice


class TestAmountCents:
    def test_decimal_to_cents_without_float_dust(self):
        assert payments.amount_cents(Decimal("462.50")) == 46250
        assert payments.amount_cents(Decimal("0.05")) == 5


class TestEnabledFlow:
    @pytest.fixture(autouse=True)
    def _stripe_enabled(self, settings):
        settings.STRIPE_SECRET_KEY = "sk_test_" + "1" * 12

    def test_pay_view_redirects_to_stripe_url(self, client, org, monkeypatch):
        invoice = _due_invoice(org)
        captured = {}

        def fake_request(method, path, params=None):
            captured["params"] = params or {}
            return {"id": "cs_test_1", "url": "https://checkout.stripe.com/c/pay/cs_test_1"}

        monkeypatch.setattr(payments, "_request", fake_request)

        response = client.get(reverse("invoice_pay_stripe", args=[invoice.public_token]))

        assert response.status_code == 302
        assert response.url == "https://checkout.stripe.com/c/pay/cs_test_1"
        assert captured["params"]["client_reference_id"] == invoice.number
        assert captured["params"]["line_items[0][price_data][unit_amount]"] == "46250"
        assert "buyer@card.test" in captured["params"]["customer_email"]

    def test_public_page_shows_card_button_when_enabled(self, client, org, settings):
        invoice = _due_invoice(org)

        body = Client().get(reverse("invoice_public", args=[invoice.public_token])).content

        assert b"Pay $" in body
        assert b"by card" in body

    def test_verified_paid_session_marks_card_link(self, client, org, monkeypatch):
        invoice = _due_invoice(org)
        monkeypatch.setattr(payments, "session_paid", lambda _session_id: True)

        response = Client().get(
            reverse("invoice_public", args=[invoice.public_token]) + "?session_id=cs_ok"
        )

        assert response.status_code == 302
        invoice.refresh_from_db()
        assert invoice.status == "paid"
        assert invoice.payment_method == PaymentMethod.CARD_LINK

    def test_unpaid_session_leaves_due(self, client, org, monkeypatch):
        invoice = _due_invoice(org)
        monkeypatch.setattr(payments, "session_paid", lambda _session_id: False)

        Client().get(reverse("invoice_public", args=[invoice.public_token]) + "?session_id=cs_no")

        invoice.refresh_from_db()
        assert invoice.status == "due"

    def test_stripe_outage_on_callback_keeps_due_with_notice(self, client, org, monkeypatch):
        invoice = _due_invoice(org)

        def boom(session_id):
            raise payments.StripeError("timeout")

        monkeypatch.setattr(payments, "session_paid", boom)

        response = Client().get(
            reverse("invoice_public", args=[invoice.public_token]) + "?session_id=cs_bad"
        )

        assert response.status_code == 302
        invoice.refresh_from_db()
        assert invoice.status == "due"


class TestDisabledFlow:
    def test_no_key_hides_button_and_pay_redirects_back(self, client, org):
        invoice = _due_invoice(org)
        anon = Client()

        body = anon.get(reverse("invoice_public", args=[invoice.public_token])).content
        assert b"Pay $" not in body

        response = anon.get(reverse("invoice_pay_stripe", args=[invoice.public_token]))
        assert response.status_code == 302
        assert reverse("invoice_public", args=[invoice.public_token]) in response.url

    def test_already_paid_invoice_has_no_button_even_when_enabled(self, client, org, settings):
        invoice = _due_invoice(org)
        invoice.mark_paid(PaymentMethod.CHECK, datetime.date.today())
        settings.STRIPE_SECRET_KEY = "sk_test_" + "1" * 12

        body = Client().get(reverse("invoice_public", args=[invoice.public_token])).content

        assert b"Pay $" not in body
        assert b"badge paid" in body
