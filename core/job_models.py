"""Routed-stop models: statuses, filter service, and the Job aggregate.

Split from ``models.py`` for the 250-LOC ceiling; string FKs mirror
``compliance_models`` and these classes are re-exported from there.
"""

import datetime

from django.db import models, transaction
from django.utils.timezone import now as tz_now

from core.billing_models import create_invoice_for_job


class FilterAction(models.TextChoices):
    """Effluent-filter service performed at the stop (MA Form 4 field)."""

    NONE = "none", "No filter / not serviced"
    CLEANED = "cleaned", "Filter cleaned"
    REPLACED = "replaced", "Filter replaced"


class JobStatus(models.TextChoices):
    """Lifecycle of a routed stop."""

    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    SKIPPED = "skipped", "Skipped"


class Job(models.Model):
    """One planned stop on one route day, carrying its completion report."""

    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="jobs")
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="jobs")
    route_day = models.DateField()
    position = models.PositiveIntegerField(default=0)
    driver = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=16, choices=JobStatus.choices, default=JobStatus.PENDING)
    gallons = models.PositiveIntegerField(null=True, blank=True)
    disposal_site = models.CharField(max_length=200, blank=True)
    completion_notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    filter_action = models.CharField(
        max_length=10,
        choices=FilterAction.choices,
        default=FilterAction.NONE,
    )

    class Meta:
        ordering = ("route_day", "position", "pk")
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "customer", "route_day"),
                name="unique_customer_per_route_day",
            ),
        )

    def __str__(self) -> str:
        return f"{self.route_day} #{self.position} {self.customer}"

    def mark_completed(  # noqa: PLR0913, PLR0917 -- explicit field kwargs beat a params blob at the curb
        self,
        gallons: int,
        disposal_site: str,
        completion_notes: str,
        pumped_on: datetime.date,
        filter_action: str = FilterAction.NONE,
        system_type: str = "",
    ) -> None:
        """Complete the stop atomically: report fields, cycle rollover, ledger, invoice."""
        from core.models import (  # noqa: PLC0415 -- avoids models<->job_models import cycle
            TankEvent,
            TankEventSource,
        )

        with transaction.atomic():
            self.status = JobStatus.COMPLETED
            self.gallons = gallons
            self.disposal_site = disposal_site
            self.completion_notes = completion_notes
            self.completed_at = tz_now()
            self.filter_action = (
                filter_action if filter_action in FilterAction.values else FilterAction.NONE
            )
            if system_type:
                self.customer.system_type = system_type[:50]
            self.customer.last_pumped = pumped_on
            self.customer.save()
            self.save()
            TankEvent.objects.create(
                customer=self.customer,
                job=self,
                event_date=pumped_on,
                gallons=gallons,
                disposal_site=disposal_site,
                notes=completion_notes,
                source=TankEventSource.JOB_COMPLETION,
            )
            create_invoice_for_job(self, gallons_pumped=gallons)
