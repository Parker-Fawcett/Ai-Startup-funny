"""Reminder tests: pure decision math, email rendering, and the send command."""

import datetime
from io import StringIO

import pytest
from django.core import mail
from django.core.management import call_command

from core.importing import parse_customers_csv
from core.models import Customer, Organization
from core.reminders import DEFAULT_MIN_RESEND_DAYS, DEFAULT_WINDOW_DAYS, decide, render_reminder

pytestmark = pytest.mark.django_db

TODAY = datetime.date(2026, 8, 22)


class TestDecide:
    def test_no_due_date_never_sends(self):
        assert decide(next_due=None, today=TODAY).should_send is False

    def test_inside_window_with_no_prior_reminder_sends(self):
        outcome = decide(next_due=TODAY + datetime.timedelta(days=10), today=TODAY)
        assert outcome.should_send
        assert outcome.reason == "due_soon"

    def test_overdue_sends_even_outside_forward_window(self):
        outcome = decide(next_due=TODAY - datetime.timedelta(days=400), today=TODAY)
        assert outcome.should_send
        assert outcome.reason == "overdue"

    def test_beyond_window_skips(self):
        outcome = decide(
            next_due=TODAY + datetime.timedelta(days=DEFAULT_WINDOW_DAYS + 1), today=TODAY
        )
        assert not outcome.should_send
        assert outcome.reason == "outside_window"

    def test_recently_reminded_suppresses_resend(self):
        recent = TODAY - datetime.timedelta(days=DEFAULT_MIN_RESEND_DAYS - 1)
        outcome = decide(
            next_due=TODAY + datetime.timedelta(days=10), today=TODAY, last_reminded_on=recent
        )
        assert not outcome.should_send
        assert outcome.reason == "recently_reminded"

    def test_old_reminder_releases_another_send(self):
        stale = TODAY - datetime.timedelta(days=DEFAULT_MIN_RESEND_DAYS)
        outcome = decide(
            next_due=TODAY + datetime.timedelta(days=10), today=TODAY, last_reminded_on=stale
        )
        assert outcome.should_send


class TestRenderReminder:
    def test_due_soon_copy_names_shop_and_date(self):
        subject, body = render_reminder(
            customer_name="Doe",
            org_name="PV Septic",
            next_due=TODAY + datetime.timedelta(days=10),
            today=TODAY,
        )
        assert "PV Septic" in subject
        assert "2026-09-01" in subject
        assert "Hi Doe," in body
        assert "call PV Septic" in body
        assert "overdue" not in subject.lower()

    def test_overdue_copy_changes_tone(self):
        subject, body = render_reminder(
            customer_name="Doe",
            org_name="PV Septic",
            next_due=TODAY - datetime.timedelta(days=30),
            today=TODAY,
        )
        assert "overdue" in subject.lower()
        assert "hasn't been serviced yet." in body


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Test Septic")


def _customer(org: Organization, *, days_out: int, email: str = "a@b.co") -> Customer:
    return Customer.objects.create(
        organization=org,
        name=f"Cust {days_out} {email}",
        address="1 Rd",
        email=email,
        last_pumped=TODAY - datetime.timedelta(days=365 * 3),
        pump_interval_months=36 + (days_out // 30),
    )


class TestSendRemindersCommand:
    def test_due_soon_customer_gets_exactly_one_mail_and_stamp(self, org):
        customer = _customer(org, days_out=10)

        call_command("send_reminders", stdout=StringIO())

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["a@b.co"]
        customer.refresh_from_db()
        assert customer.last_reminded_on is not None

    def test_immediate_rerun_is_suppressed_by_resend_guard(self, org):
        _customer(org, days_out=10)

        call_command("send_reminders", stdout=StringIO())
        call_command("send_reminders", stdout=StringIO())

        assert len(mail.outbox) == 1

    def test_missing_email_and_far_future_are_skipped(self, org):
        _customer(org, days_out=10, email="")
        _customer(org, days_out=200)

        out = StringIO()
        call_command("send_reminders", stdout=out)

        assert len(mail.outbox) == 0
        text = out.getvalue()
        assert "sent=0" in text
        assert "'no_email': 1" in text

    def test_dry_run_reports_without_sending_or_stamping(self, org):
        customer = _customer(org, days_out=10)

        out = StringIO()
        call_command("send_reminders", dry_run=True, stdout=out)

        assert len(mail.outbox) == 0
        assert "[dry]" in out.getvalue()
        customer.refresh_from_db()
        assert customer.last_reminded_on is None

    def test_overdue_customer_included(self, org):
        overdue = Customer.objects.create(
            organization=org,
            name="Old Timer",
            address="2 Rd",
            email="old@b.co",
            last_pumped=datetime.date(2020, 1, 1),
            pump_interval_months=12,
        )

        call_command("send_reminders", stdout=StringIO())

        subjects = [m.subject for m in mail.outbox]
        assert any("overdue" in s.lower() for s in subjects)
        assert mail.outbox[0].to == [overdue.email]


class TestImportEmailColumn:
    def test_csv_email_column_flows_to_customer(self, org):
        result = parse_customers_csv(
            "name,address,email\nEmailed Shop,5 Rd,e@f.co\nPlain Shop,6 Rd,\n"
        )

        assert len(result.rows) == 2
        emailed = result.rows[0]
        assert emailed.email == "e@f.co"
        saved = Customer.from_import_row(organization=org, row=emailed)
        assert saved.email == "e@f.co"
