"""Domain models; compliance/billing/marketing siblings re-exported here."""

from typing import TYPE_CHECKING

from django.db import models

from core.billing_models import (  # noqa: F401 -- app-registry re-exports
    Invoice,
    PaymentMethod,
    RateCard,
    create_invoice_for_job,
)
from core.compliance_models import ComplianceMixin, FilingReceipt, Jurisdiction  # noqa: F401
from core.job_models import FilterAction, Job, JobStatus  # noqa: F401 -- registry re-exports
from core.scheduling import compute_next_due

if TYPE_CHECKING:
    from core.importing import CustomerRow


class Organization(models.Model):
    """A septic hauling shop; the tenant root for all route data."""

    name = models.CharField(max_length=200)
    home_lat = models.FloatField(null=True, blank=True)
    home_lng = models.FloatField(null=True, blank=True)

    plan = models.CharField(max_length=16, blank=True)
    stripe_customer_id = models.CharField(max_length=64, blank=True)
    stripe_subscription_id = models.CharField(max_length=64, blank=True)
    subscription_status = models.CharField(max_length=16, blank=True)
    trial_ends_on = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)

    @property
    def home_coords(self) -> tuple[float, float] | None:
        """Yard coordinates once set; route anchoring falls back to first stop."""
        if self.home_lat is None or self.home_lng is None:
            return None
        return (float(self.home_lat), float(self.home_lng))


class Customer(ComplianceMixin, models.Model):
    """A septic-system account on a shop's route book.

    Denormalized invariants recomputed on save(): ``next_due`` = ``last_pumped``
    + interval (the SQL-filterable due book); ``tank_key`` = parcel/address
    identity so history groups across duplicate accounts; ``compliance_due``
    from ``ComplianceMixin`` carries the jurisdiction filing deadline.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="customers"
    )
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    parcel_id = models.CharField(max_length=64, blank=True)
    assessor_map = models.CharField(max_length=32, blank=True)
    assessor_lot = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    sms_opt_out = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    tank_size_gallons = models.PositiveIntegerField(null=True, blank=True)
    system_type = models.CharField(max_length=50, blank=True)
    pump_interval_months = models.PositiveIntegerField(default=36)
    last_pumped = models.DateField(null=True, blank=True)
    next_due = models.DateField(null=True, blank=True, db_index=True)
    last_reminded_on = models.DateField(null=True, blank=True)
    tank_key = models.CharField(max_length=450, blank=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args: object, **kwargs: object) -> None:
        """Recompute the stored due date and tank identity whenever persistence occurs."""
        if self.last_pumped is None:
            self.next_due = None
        else:
            self.next_due = compute_next_due(self.last_pumped, self.pump_interval_months)
        self.tank_key = _tank_identity_key(
            parcel_id=self.parcel_id,
            address=self.address,
            city=self.city,
            zip_code=self.zip_code,
        )
        super().save(*args, **kwargs)

    @classmethod
    def from_import_row(cls, organization: Organization, row: "CustomerRow") -> "Customer":
        """Build one unsaved customer with ``next_due``/``tank_key`` precomputed.

        ``bulk_create`` skips ``save()``, so imports must route through here.
        """
        customer = cls(
            organization=organization,
            name=row.name,
            address=row.address,
            city=row.city,
            state=row.state,
            zip_code=row.zip_code,
            email=row.email,
            phone=row.phone,
            tank_size_gallons=row.tank_size_gallons,
            pump_interval_months=row.pump_interval_months,
            last_pumped=row.last_pumped,
            next_due=(
                compute_next_due(row.last_pumped, row.pump_interval_months)
                if row.last_pumped is not None
                else None
            ),
        )
        customer.tank_key = _tank_identity_key(
            parcel_id="", address=row.address, city=row.city, zip_code=row.zip_code
        )
        return customer

    @property
    def coords(self) -> tuple[float, float] | None:
        """Return ``(lat, lng)`` once geocoded, else ``None``."""
        if self.lat is None or self.lng is None:
            return None
        return (self.lat, self.lng)

    @property
    def tank_ledger(self) -> "models.QuerySet[TankEvent]":
        """Pump-out history for this physical tank, newest first.

        Every account sharing this tank's key (same parcel, or same address
        when unparcelled) reads one shared ledger — history follows the tank,
        not whoever currently holds the account.
        """
        siblings = Customer.objects.filter(organization=self.organization, tank_key=self.tank_key)
        return TankEvent.objects.filter(customer__in=siblings)


def _tank_identity_key(*, parcel_id: str, address: str, city: str, zip_code: str) -> str:
    """Return the stable identity of a physical tank from its siting fields.

    Parcel numbers win when present (assessor data is authoritative); the
    normalized address is the fallback. Kept module-level so data migrations
    can recompute keys without instantiating model classes.
    """
    if parcel_id.strip():
        return f"parcel:{parcel_id.strip().lower()}"
    return f"addr:{address.strip().lower()}|{city.strip().lower()}|{zip_code.strip()}"


class TankEventSource(models.TextChoices):
    """Where a ledger entry originated."""

    JOB_COMPLETION = "job_completion", "Job completion"
    MANUAL_ENTRY = "manual_entry", "Manual entry"
    IMPORT_BACKFILL = "import_backfill", "Import backfill"


class TankEvent(models.Model):
    """One immutable pump-out record on a tank's running ledger.

    The ledger is the shop's balance sheet: every completed job appends here,
    so each year of service compounds into records a departing shop would
    have to abandon — that is the churn lever (data gravity).
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="tank_events")
    job = models.ForeignKey(
        "Job", on_delete=models.SET_NULL, null=True, blank=True, related_name="tank_events"
    )
    event_date = models.DateField()
    gallons = models.PositiveIntegerField(null=True, blank=True)
    disposal_site = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    source = models.CharField(
        max_length=20, choices=TankEventSource.choices, default=TankEventSource.JOB_COMPLETION
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-event_date", "-pk")
        indexes = (models.Index(fields=("customer", "event_date"), name="tankevent_cust_date"),)

    def __str__(self) -> str:
        return f"{self.event_date} {self.customer} {self.gallons or '?'}gal"


class FunnelEvent(models.Model):
    """One recorded conversion-funnel event (see ``core.funnel``)."""

    name = models.CharField(max_length=32, db_index=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="funnel_events"
    )
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-pk")

    def __str__(self) -> str:
        return f"{self.name} @ {self.created_at:%Y-%m-%d %H:%M}"
