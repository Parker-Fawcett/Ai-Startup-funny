"""Billing models: the shop's rate card and per-job invoices (Fix #1).

Same-day invoicing is the market-validated demo moment: a job closes, the
invoice exists before the truck leaves the driveway, and payment settles by
card link, check, cash, or ACH. Split out of ``models.py`` to honor the
250-LOC ceiling; string FK refs mirror ``compliance_models`` and these
classes are re-exported from there for imports elsewhere.
"""

import datetime
import secrets
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse

from core.pricing import RateSpec, price_job

if TYPE_CHECKING:
    from core.models import Job, Organization


def make_token() -> str:
    """Unguessable share token so customer links grant nothing else."""
    return secrets.token_urlsafe(24)


class PaymentMethod(models.TextChoices):
    """How the money actually arrived."""

    CARD_LINK = "card_link", "Card (online link)"
    CHECK = "check", "Check"
    CASH = "cash", "Cash"
    ACH = "ach", "ACH transfer"


class InvoiceStatus(models.TextChoices):
    """Lifecycle; VOID hides a mispriced bill without deleting history."""

    DUE = "due", "Due"
    PAID = "paid", "Paid"
    VOID = "void", "Void"


class RateCard(models.Model):
    """Per-shop price list used to auto-generate invoices on completion."""

    organization = models.OneToOneField(
        "Organization", on_delete=models.CASCADE, related_name="rate_card"
    )
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("350.00"))
    included_gallons = models.PositiveIntegerField(default=1000)
    overage_per_gallon = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.05")
    )
    trip_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("45.00"))
    disposal_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("50.00"))

    class Meta:
        verbose_name_plural = "rate cards"

    def __str__(self) -> str:
        return f"Rate card — {self.organization}"

    def as_spec(self) -> RateSpec:
        """Render the editable row as the pure pricing input."""
        return RateSpec(
            included_gallons=self.included_gallons,
            base_price=self.base_price,
            overage_per_gallon=self.overage_per_gallon,
            trip_fee=self.trip_fee,
            disposal_fee=self.disposal_fee,
        )

    @classmethod
    def get_for(cls, organization: "Organization") -> "RateCard":
        """Return the shop's card, creating market-default rates on first touch."""
        card = cls.objects.filter(organization=organization).first()
        if card is None:
            card = cls.objects.create(organization=organization)
        return card


class Invoice(models.Model):
    """One completed job's bill, with an unguessable customer-facing link."""

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="invoices"
    )
    job = models.OneToOneField("Job", on_delete=models.CASCADE, related_name="invoice")
    number = models.CharField(max_length=16, unique=True)
    public_token = models.CharField(max_length=64, unique=True, default=make_token)
    issued_on = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=8, choices=InvoiceStatus.choices, default=InvoiceStatus.DUE, db_index=True
    )
    lines = models.JSONField(default=list)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=12, choices=PaymentMethod.choices, blank=True)

    class Meta:
        ordering = ("-issued_on", "-pk")

    def __str__(self) -> str:
        return f"{self.number} ${self.total} {self.get_status_display()}"

    def get_absolute_url(self) -> str:
        """Return the link the owner texts or emails to the customer."""
        return reverse("invoice_public", args=[self.public_token])

    def mark_paid(self, method: str, paid_on_date: datetime.date) -> None:
        """Settle the invoice; already-settled rows stay untouched."""
        if self.status == InvoiceStatus.PAID:
            return
        self.status = InvoiceStatus.PAID
        self.payment_method = method
        self.paid_on = paid_on_date
        self.save(update_fields=("status", "payment_method", "paid_on"))


def create_invoice_for_job(job: "Job", *, gallons_pumped: int) -> "Invoice":
    """Build the completion invoice from the shop's rate card, idempotently.

    Called inside ``Job.mark_completed``'s atomic block; re-completions and
    admin saves must never mint a second invoice for one stop.
    """
    existing = Invoice.objects.filter(job=job).first()
    if existing is not None:
        return existing
    card = RateCard.get_for(job.organization)
    result = price_job(
        gallons_pumped=gallons_pumped,
        tank_size_gallons=job.customer.tank_size_gallons,
        spec=card.as_spec(),
    )
    return Invoice.objects.create(
        organization=job.organization,
        job=job,
        number=f"INV-{job.pk:06d}",
        lines=[{"label": line.label, "amount": str(line.amount)} for line in result.lines],
        total=result.total,
    )
