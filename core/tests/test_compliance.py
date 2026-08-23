"""Move 3 coverage: NE compliance dataset, deadline clock, receipts, PDF footer."""

import datetime
from datetime import date

import pytest
from django.db import IntegrityError
from django.urls import reverse

from core.compliance import (
    FilingRule,
    compute_filing_deadline,
    days_remaining,
    filing_summary,
    resolve_jurisdiction,
)
from core.compliance_models import FilingReceipt, Jurisdiction
from core.models import Customer, Job, Organization
from core.reports import render_job_report_pdf

MA_STATEWIDE = FilingRule(
    state="MA",
    town="",
    filing_rule="310 CMR 15.351",
    deadline_days=14,
    form_variant="DEP Title 5 Pump-Out Form",
    effective_from=date(2016, 1, 1),
)
LEOMINSTER_STRICT = FilingRule(
    state="MA",
    town="Leominster",
    filing_rule="Leominster BOH Title 5 bylaw",
    deadline_days=7,
    form_variant="Leominster BOH Pump-Out Certificate",
    effective_from=date(2023, 7, 1),
)
LEOMINSTER_OLD = FilingRule(
    state="MA",
    town="Leominster",
    filing_rule="old bylaw",
    deadline_days=10,
    form_variant="Old Form",
    effective_from=date(2020, 1, 1),
    effective_to=date(2023, 6, 30),
)


class TestPureDeadlineMath:
    """The statutory clock, no DB required."""

    def test_ma_baseline_fourteen_day_clock(self):
        assert compute_filing_deadline(date(2026, 8, 1), 14) == date(2026, 8, 15)

    def test_days_remaining_negative_once_window_closed(self):
        assert days_remaining(date(2026, 8, 15), date(2026, 8, 20)) == -5


class TestPureJurisdictionResolution:
    """Most-specific in-force rule wins; towns are matched case-insensitively."""

    RULES = (MA_STATEWIDE, LEOMINSTER_STRICT, LEOMINSTER_OLD)

    def test_town_rule_beats_statewide_default(self):
        winner = resolve_jurisdiction(
            state="MA", town="leominster", rules=self.RULES, as_of=date(2026, 8, 1)
        )
        assert winner == LEOMINSTER_STRICT

    def test_expired_override_falls_back_to_statewide(self):
        winner = resolve_jurisdiction(
            state="MA", town="Leominster", rules=self.RULES, as_of=date(2020, 6, 1)
        )
        assert winner == LEOMINSTER_OLD  # the rule in force back then, not today's

    def test_future_rule_not_yet_in_force(self):
        winner = resolve_jurisdiction(
            state="MA", town="Leominster", rules=self.RULES, as_of=date(2023, 6, 30)
        )
        assert winner == LEOMINSTER_OLD

    def test_unknown_town_gets_statewide_and_unknown_state_gets_none(self):
        fallback = resolve_jurisdiction(
            state="MA", town="Springfield", rules=self.RULES, as_of=date(2026, 8, 1)
        )
        assert fallback == MA_STATEWIDE
        assert (
            resolve_jurisdiction(
                state="TX", town="Austin", rules=self.RULES, as_of=date(2026, 8, 1)
            )
            is None
        )

    def test_filing_summary_names_form_scope_and_due_date(self):
        summary = filing_summary(MA_STATEWIDE, date(2026, 8, 1))
        assert "310 CMR 15.351" in summary
        assert "MA statewide" in summary
        assert "2026-08-15" in summary


@pytest.mark.django_db
class TestSeededDataset:
    """The migration-seeded NE baseline behaves as the moat spec requires."""

    def test_seed_loaded_five_new_england_rules(self):
        assert Jurisdiction.objects.count() == 5
        assert set(Jurisdiction.objects.values_list("state", flat=True)) == {"MA", "NH", "ME"}
        statewide_ma = Jurisdiction.objects.get(state="MA", town="")
        assert statewide_ma.deadline_days == 14
        assert statewide_ma.filing_rule == "310 CMR 15.351"
        assert "14 days" in statewide_ma.change_log

    def test_resolve_prefers_seeded_town_override(self):
        winner = Jurisdiction.objects.resolve(state="MA", town="leominster", as_of=date(2026, 8, 1))
        assert winner is not None
        assert winner.deadline_days == 7
        assert winner.town == "Leominster"

    def test_resolve_unknown_town_falls_back_to_statewide(self):
        winner = Jurisdiction.objects.resolve(
            state="MA", town="Springfield", as_of=date(2026, 8, 1)
        )
        assert winner is not None
        assert winner.town == ""
        assert winner.deadline_days == 14

    def test_customer_compliance_due_uses_rule_in_force_on_service_date(self):
        organization = Organization.objects.create(name="Window Septic")
        strict_now = Customer.objects.create(
            organization=organization,
            name="Strict Town",
            address="1 Main St",
            city="Leominster",
            state="MA",
            last_pumped=date(2026, 7, 20),
        )
        historical = Customer.objects.create(
            organization=organization,
            name="Serviced Before Tightening",
            address="2 Main St",
            city="Leominster",
            state="MA",
            last_pumped=date(2022, 6, 1),
        )
        # Today's Leominster rule: 7 days.
        assert strict_now.compliance_due == date(2026, 7, 27)
        # But a 2022 service keeps the statewide 14-day window that applied then.
        assert historical.compliance_due == date(2022, 6, 15)

    def test_compliance_due_is_none_without_pump_or_rule(self):
        organization = Organization.objects.create(name="Edge Septic")
        never_pumped = Customer.objects.create(
            organization=organization, name="Never", address="3 Main St", state="MA"
        )
        out_of_region = Customer.objects.create(
            organization=organization,
            name="Texan",
            address="4 Main St",
            city="Austin",
            state="TX",
            last_pumped=date(2026, 7, 1),
        )
        assert never_pumped.compliance_due is None
        assert out_of_region.compliance_due is None


@pytest.mark.django_db
class TestFilingWorkflow:
    def test_receipt_creation_and_one_to_one_uniqueness(self):
        organization = Organization.objects.create(name="Receipt Septic")
        customer = Customer.objects.create(
            organization=organization,
            name="Filed Shop",
            address="5 Main St",
            city="Springfield",
            state="MA",
        )
        job = Job.objects.create(
            organization=organization, customer=customer, route_day=date(2026, 8, 1)
        )
        jurisdiction = Jurisdiction.objects.resolve(
            state="MA", town="Springfield", as_of=date(2026, 8, 1)
        )

        receipt = FilingReceipt.objects.create(
            job=job,
            jurisdiction=jurisdiction,
            filed_on=date(2026, 8, 10),
            filed_by="P. Fawcett",
            receipt_ref="BOH stamp 4411",
        )
        assert receipt.jurisdiction.deadline_days == 14
        assert str(receipt).startswith("JOB-")
        with pytest.raises(IntegrityError):
            FilingReceipt.objects.create(
                job=job,
                jurisdiction=jurisdiction,
                filed_on=date(2026, 8, 11),
                filed_by="Duplicate",
            )

    def test_dashboard_lists_open_filing_window_with_days_left(self, client, org):
        customer = Customer.objects.create(
            organization=org,
            name="Leominster Stop",
            address="6 Main St",
            city="Leominster",
            state="MA",
        )
        job = Job.objects.create(
            organization=org,
            customer=customer,
            route_day=datetime.date.today() - datetime.timedelta(days=2),
        )
        job.mark_completed(
            gallons=900,
            disposal_site="North WWTP",
            completion_notes="routine",
            pumped_on=job.route_day,
        )

        response = client.get(reverse("dashboard"))

        assert response.status_code == 200
        body = response.content.decode()
        assert "Leominster Stop" in body
        assert "Leominster BOH Pump-Out Certificate" in body
        assert f">{14 - 2 - 7}d</strong>" in body  # 5 days left on the 7-day clock

    def test_pdf_footer_carries_jurisdiction_line(self):
        organization = Organization.objects.create(name="PDF Septic")
        customer = Customer.objects.create(
            organization=organization,
            name="Report Buyer",
            address="10 Station Rd",
            city="Springfield",
            state="MA",
        )
        job = Job.objects.create(
            organization=organization,
            customer=customer,
            route_day=date(2026, 8, 1),
            gallons=900,
        )

        body = render_job_report_pdf(job)

        assert b"310 CMR 15.351" in body
        assert b"DEP Title 5 Pump-Out Form" in body
        assert b"2026-08-15" in body  # statutory due date, 14-day window
