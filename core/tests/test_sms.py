"""SMS channel tests: transport mocked, opt-out honored, copy TCPA-safe."""

import datetime
import urllib.error
from io import StringIO
from typing import Self

import pytest
from django.contrib.admin.sites import AdminSite
from django.core.management import call_command
from django.test import Client
from django.urls import reverse

from core import sms as sms_channel
from core.admin import CustomerAdmin
from core.importing import parse_customers_csv
from core.models import Customer, Organization
from core.reminders import render_sms

pytestmark = pytest.mark.django_db

TODAY = datetime.date(2026, 8, 22)


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Test Septic")


def _customer(org: Organization, *, phone: str = "+14135550100", opted_out: bool = False):
    return Customer.objects.create(
        organization=org,
        name="Texted Shop",
        address="1 Rd",
        phone=phone,
        sms_opt_out=opted_out,
        last_pumped=TODAY - datetime.timedelta(days=365),
        pump_interval_months=12,
    )


class TestRenderSms:
    def test_message_is_short_and_has_optout(self):
        text = render_sms(
            org_name="PV Septic", next_due=TODAY + datetime.timedelta(days=10), today=TODAY
        )
        assert "Reply STOP" in text
        assert len(text) <= 160

    def test_overdue_variant(self):
        text = render_sms(
            org_name="PV Septic", next_due=TODAY - datetime.timedelta(days=5), today=TODAY
        )
        assert "overdue" in text


class _FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> bool:
        return False


class TestSmsChannel:
    def test_send_via_twilio(self, monkeypatch, settings):
        settings.TWILIO_ACCOUNT_SID = "AC123"
        settings.TWILIO_AUTH_TOKEN = "test-token-not-real"  # noqa: S105 -- fake credential
        settings.TWILIO_FROM_NUMBER = "+15005550006"
        sent: dict[str, str] = {}

        def fake_urlopen(request, timeout=0):
            sent["body"] = request.data.decode()
            sent["auth"] = request.get_header("Authorization")
            return _FakeResponse(b'{"sid": "SM1", "status": "queued"}')

        monkeypatch.setattr(sms_channel.urllib.request, "urlopen", fake_urlopen)

        result = sms_channel.send_sms("+14135550100", "due soon")

        assert result["sid"] == "SM1"
        assert "%2B14135550100" in sent["body"]
        assert sent["auth"].startswith("Basic ")

    def test_disabled_raises(self, settings):
        settings.TWILIO_ACCOUNT_SID = ""
        with pytest.raises(sms_channel.SmsError):
            sms_channel.send_sms("+14135550100", "x")

    def test_network_error_wrapped(self, monkeypatch, settings):
        settings.TWILIO_ACCOUNT_SID = "AC"
        settings.TWILIO_AUTH_TOKEN = "another-fake"  # noqa: S105 -- fake credential
        settings.TWILIO_FROM_NUMBER = "+1"

        def boom(request, timeout=0):
            raise urllib.error.URLError("no route")

        monkeypatch.setattr(sms_channel.urllib.request, "urlopen", boom)
        with pytest.raises(sms_channel.SmsError):
            sms_channel.send_sms("+14135550100", "x")


class TestRemindersCommandSms:
    @pytest.fixture(autouse=True)
    def _twilio_configured(self, settings):
        settings.TWILIO_ACCOUNT_SID = "AC-test"
        settings.TWILIO_AUTH_TOKEN = "test-token"  # noqa: S105 -- fake credential
        settings.TWILIO_FROM_NUMBER = "+15005550006"

    def test_sms_channel_sends_and_stamps(self, org, monkeypatch):
        customer = _customer(org)
        outgoing: list[tuple[str, str]] = []

        def capture(to, body):
            outgoing.append((to, body))

        monkeypatch.setattr(sms_channel, "send_sms", capture)
        call_command("send_reminders", channel="sms", stdout=StringIO())

        assert [to for to, _ in outgoing] == [customer.phone]
        assert "Reply STOP" in outgoing[0][1]
        customer.refresh_from_db()
        assert customer.last_reminded_on is not None

    def test_opt_out_customer_never_texted(self, org, monkeypatch):
        _customer(org, opted_out=True)

        def refuse(to, _body):
            raise AssertionError(f"should not text {to}")

        monkeypatch.setattr(sms_channel, "send_sms", refuse)
        out = StringIO()
        call_command("send_reminders", channel="sms", stdout=out)

        assert "'sms_opt_out': 1" in out.getvalue()

    def test_missing_phone_skipped(self, org, monkeypatch):
        _customer(org, phone="")
        outgoing: list[str] = []

        def capture(to, _body):
            outgoing.append(to)

        monkeypatch.setattr(sms_channel, "send_sms", capture)
        out = StringIO()
        call_command("send_reminders", channel="sms", stdout=out)

        assert outgoing == []
        assert "'no_phone': 1" in out.getvalue()

    def test_both_channels_deliver_once_each(self, org, monkeypatch):
        customer = _customer(org, phone="+14135550111")
        customer.email = "both@x.co"
        customer.save(update_fields=["email"])
        texts: list[str] = []
        mails: list[list[str]] = []

        def capture_sms(to, _body):
            texts.append(to)

        def fake_send_mail(_subject, _body, _from_email, recipients):
            mails.append(recipients)

        monkeypatch.setattr(sms_channel, "send_sms", capture_sms)
        monkeypatch.setattr("core.management.commands.send_reminders.send_mail", fake_send_mail)
        call_command("send_reminders", channel="both", stdout=StringIO())

        assert texts == ["+14135550111"]
        assert mails == [["both@x.co"]]
        customer.refresh_from_db()
        assert customer.last_reminded_on == datetime.date.today()


class TestCsvPhoneColumn:
    def test_phone_flows_through_import_row(self, org):
        result = parse_customers_csv("name,address,phone\nPinged,7 Rd,+14135550123\n")
        saved = Customer.from_import_row(organization=org, row=result.rows[0])
        assert saved.phone == "+14135550123"


class TestAdminOptOutAction:
    @pytest.fixture
    def staff_client(self, client: Client, django_user_model):
        client.force_login(
            django_user_model.objects.create_superuser("sms-admin", "sa@x.co", "pw12345!!")
        )
        return client

    def test_action_flags_opt_out_via_changelist(self, staff_client, org):
        target = Customer.objects.create(organization=org, name="OptOut Me", address="r")
        changelist = reverse("admin:core_customer_changelist")

        response = staff_client.post(
            changelist,
            {"action": "mark_sms_opt_out", "_selected_action": [str(target.pk)]},
            follow=True,
        )

        assert response.status_code == 200
        target.refresh_from_db()
        assert target.sms_opt_out is True


def test_admin_site_wiring(org):
    site = AdminSite()
    model_admin = CustomerAdmin(Customer, site)
    assert hasattr(model_admin, "mark_sms_opt_out")


def test_sms_without_config_reports_disabled(org, settings):
    _customer(org)
    settings.TWILIO_ACCOUNT_SID = ""

    out = StringIO()
    call_command("send_reminders", channel="sms", stdout=out)

    assert "TWILIO_* settings are missing" in out.getvalue()
