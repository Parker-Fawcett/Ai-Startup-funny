"""Billing tests: pure pricing math, invoice generation, settlement, public link."""

import datetime
from decimal import Decimal

import pytest
from django.test import Client
from django.urls import reverse

from core.billing_models import Invoice, PaymentMethod, RateCard
from core.models import Customer, Job, Organization
from core.pricing import RateSpec, price_job

pytestmark = pytest.mark.django_db


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Test Septic")


@pytest.fixture
def client(client: Client, user) -> Client:
    return client


def _make_customer_job(org: Organization, tank: int | None = 1000):
    customer = Customer.objects.create(
        organization=org,
        name="Ledger Buyer",
        address="1 Rd",
        tank_size_gallons=tank,
    )
    job = Job.objects.create(organization=org, customer=customer, route_day=datetime.date.today())
    return customer, job


class TestPricingMath:
    def test_base_plus_fees_when_below_capacity(self):
        result = price_job(gallons_pumped=900, tank_size_gallons=1000, spec=RateSpec())
        labels = [line.label for line in result.lines]
        assert labels == ["Pump-out service", "Trip fee", "Disposal fee"]
        assert str(result.total) == "445.00"

    def test_overage_applies_beyond_tank_capacity(self):
        result = price_job(gallons_pumped=1350, tank_size_gallons=1000, spec=RateSpec())
        overage = next(line for line in result.lines if "Overage" in line.label)
        assert str(overage.amount) == "17.50"
        assert str(result.total) == "462.50"

    def test_unknown_tank_falls_back_to_spec_included_gallons(self):
        spec = RateSpec(included_gallons=500)
        result = price_job(gallons_pumped=600, tank_size_gallons=None, spec=spec)
        assert any("Overage (100 gal" in line.label for line in result.lines)

    def test_zero_fees_are_suppressed_from_lines(self):
        spec = RateSpec(trip_fee=Decimal("0.00"), disposal_fee=Decimal("0.00"))
        result = price_job(gallons_pumped=100, tank_size_gallons=1000, spec=spec)
        assert [line.label for line in result.lines] == ["Pump-out service"]
        assert str(result.total) == "350.00"


class TestInvoiceGeneration:
    def test_completing_job_mints_invoice_with_expected_math(self, client, org):
        _, job = _make_customer_job(org)

        response = client.post(
            reverse("job_complete", args=[job.pk]),
            {"gallons": "1350", "disposal_site": "North WWTP", "notes": "ok"},
        )

        assert response.status_code == 302
        invoice = Invoice.objects.get(job=job)
        assert invoice.number == f"INV-{job.pk:06d}"
        assert invoice.status == "due"
        assert str(invoice.total) == "462.50"
        labels = [line["label"] for line in invoice.lines]
        assert any("Overage" in label for label in labels)
        assert len(invoice.public_token) >= 20

    def test_recompletion_never_mints_a_second_invoice(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=800, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )

        job.mark_completed(
            gallons=900, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )

        assert Invoice.objects.filter(job=job).count() == 1


class TestMarkPaid:
    def test_post_check_settles_invoice(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=800, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )
        invoice = Invoice.objects.get(job=job)

        response = client.post(
            reverse("invoice_pay", args=[invoice.pk]), {"payment_method": "check"}
        )

        assert response.status_code == 302
        invoice.refresh_from_db()
        assert invoice.status == "paid"
        assert invoice.payment_method == PaymentMethod.CHECK
        assert invoice.paid_on == datetime.date.today()

    def test_invalid_method_leaves_invoice_due(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=800, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )
        invoice = Invoice.objects.get(job=job)

        response = client.post(
            reverse("invoice_pay", args=[invoice.pk]), {"payment_method": "bitcoin"}
        )

        assert response.status_code == 302
        invoice.refresh_from_db()
        assert invoice.status == "due"


class TestPublicInvoiceLink:
    def test_anonymous_token_page_shows_due_total(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=1350, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )
        invoice = Invoice.objects.get(job=job)

        response = Client().get(reverse("invoice_public", args=[invoice.public_token]))

        assert response.status_code == 200
        body = response.content.decode()
        assert "$462.50" in body
        assert "Due" in body
        assert "Test Septic" in body

    def test_unknown_token_is_404(self):
        response = Client().get(reverse("invoice_public", args=["nope"]))

        assert response.status_code == 404

    def test_page_reflects_paid_state_after_settlement(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=800, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )
        invoice = Invoice.objects.get(job=job)
        invoice.mark_paid(PaymentMethod.CASH, datetime.date.today())

        response = Client().get(reverse("invoice_public", args=[invoice.public_token]))

        body = response.content.decode()
        assert "Paid" in body
        assert "Cash" in body


class TestRateCard:
    def test_get_for_creates_once_then_returns_same_row(self, org):
        first = RateCard.get_for(org)
        second = RateCard.get_for(org)

        assert first.pk == second.pk
        assert str(first.as_spec().base_price) == "350.00"


class TestBookkeeperExport:
    def test_month_csv_contains_invoice_rows(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=1350, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )
        invoice = Invoice.objects.get(job=job)
        today = datetime.date.today()

        response = client.get(reverse("invoice_export", args=[today.year, today.month]))

        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        rows = [r.decode().strip().split(",") for r in response.content.splitlines()]
        assert rows[0][0] == "invoice_number"
        target = next(r for r in rows[1:] if r and r[0] == invoice.number)
        assert target[2] == "Ledger Buyer"
        assert target[6] == "462.50"

    def test_other_month_excluded(self, client, org):
        _, job = _make_customer_job(org)
        job.mark_completed(
            gallons=800, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
        )
        last_year = datetime.date.today().year - 1

        response = client.get(reverse("invoice_export", args=[last_year, 1]))

        body = response.content.decode()
        assert "INV-" not in body.replace("invoice_number", "")

    def test_requires_login(self):
        response = Client().get(reverse("invoice_export", args=[datetime.date.today().year, 1]))
        assert response.status_code == 302
