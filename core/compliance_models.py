"""Compliance dataset models: per-jurisdiction filing rules and receipts.

Move 3's moat is maintained regulatory truth. Each ``Jurisdiction`` row is a
point-in-time record with an explicit change log, so a historical job keeps
the rule that was in force when it was serviced; superseded rules are closed
with ``effective_to`` and never edited in place.

Split out of ``models.py`` to honor the 250-LOC ceiling; importing these
classes from there registers them with the ``core`` app as usual.
"""

import datetime

from django.db import models
from django.db.models import F, Q
from django.utils.timezone import now as tz_now

from core.compliance import (
    FilingRule,
    compute_filing_deadline,
    resolve_jurisdiction,
)


class JurisdictionQuerySet(models.QuerySet):
    """Lookups that respect effective-date windowing."""

    def in_force(self, as_of: datetime.date) -> "JurisdictionQuerySet":
        """Rows whose window contains ``as_of`` (open-ended end = still current)."""
        ended = Q(effective_to__isnull=True) | Q(effective_to__gte=as_of)
        return self.filter(Q(effective_from__lte=as_of) & ended)

    def resolve(self, *, state: str, town: str, as_of: datetime.date) -> "Jurisdiction | None":
        """Most-specific in-force row for a siting: exact town beats statewide."""
        candidates = list(self.in_force(as_of).filter(state__iexact=state.strip()))
        winner = resolve_jurisdiction(
            state=state, town=town, rules=[row.as_rule() for row in candidates], as_of=as_of
        )
        if winner is None:
            return None
        return next(row for row in candidates if row.as_rule() == winner)


class Jurisdiction(models.Model):
    """One filing rule for one NE state or town, valid over one date window.

    Town-scoped rows (``town`` non-blank) override their state's default.
    New England first per the moat spec — MA/NH/ME/CT/RI only.
    """

    state = models.CharField(max_length=2)
    town = models.CharField(max_length=100, blank=True)  # blank = statewide default
    county = models.CharField(max_length=100, blank=True)
    filing_rule = models.CharField(max_length=120)  # e.g. "310 CMR 15.351"
    deadline_days = models.PositiveIntegerField(default=14)
    form_variant = models.CharField(max_length=120)  # board's expected form name
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    change_log = models.TextField(blank=True)

    objects = JurisdictionQuerySet.as_manager()

    class Meta:
        ordering = ("state", "town", "-effective_from")
        constraints = (
            models.UniqueConstraint(
                fields=("state", "town", "effective_from"),
                name="unique_rule_per_scope_start",
            ),
            models.CheckConstraint(
                condition=Q(effective_to__isnull=True) | Q(effective_to__gte=F("effective_from")),
                name="effective_window_sane",
            ),
        )

    def __str__(self) -> str:
        scope = f"{self.state} · {self.town}" if self.town else f"{self.state} statewide"
        return f"{scope}: {self.filing_rule}"

    def as_rule(self) -> FilingRule:
        """Project onto the DB-free value type the pure helpers operate on."""
        return FilingRule(
            state=self.state,
            town=self.town,
            filing_rule=self.filing_rule,
            deadline_days=self.deadline_days,
            form_variant=self.form_variant,
            effective_from=self.effective_from,
            effective_to=self.effective_to,
        )


class ComplianceMixin(models.Model):
    """Jurisdiction-aware statutory clock for sited accounts (Customer)."""

    class Meta:
        abstract = True

    def resolve_jurisdiction(self, as_of: datetime.date | None = None) -> Jurisdiction | None:
        """Return the filing rule in force where this account sits, as of ``as_of``."""
        return Jurisdiction.objects.resolve(
            state=self.state,
            town=self.city,
            as_of=as_of if as_of is not None else tz_now().date(),
        )

    @property
    def compliance_due(self) -> datetime.date | None:
        """Statutory filing deadline for the most recent pump-out, else None.

        Resolved against the rule in force on ``last_pumped`` so old service
        dates keep their historical window even after a town tightens its rule.
        """
        if self.last_pumped is None:
            return None
        rule = self.resolve_jurisdiction(as_of=self.last_pumped)
        if rule is None:
            return None
        return compute_filing_deadline(self.last_pumped, rule.deadline_days)


class FilingReceipt(models.Model):
    """Proof that one job's report reached its Board of Health on time."""

    job = models.OneToOneField("Job", on_delete=models.CASCADE, related_name="filing_receipt")
    jurisdiction = models.ForeignKey(
        Jurisdiction, on_delete=models.PROTECT, related_name="receipts"
    )
    filed_on = models.DateField()
    filed_by = models.CharField(max_length=120)
    receipt_ref = models.CharField(max_length=120, blank=True)  # stamp / portal / agent ref
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-filed_on", "-pk")

    def __str__(self) -> str:
        return f"JOB-{self.job_id:06d} filed {self.filed_on} ({self.jurisdiction})"
