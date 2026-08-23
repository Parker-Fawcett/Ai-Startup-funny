"""Move 1 coverage: tank-ledger data gravity, parcel grouping, route-sale export."""

import csv
import datetime
import io
import zipfile

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.importing import CustomerRow
from core.models import Customer, Job, Organization, TankEvent, TankEventSource

pytestmark = pytest.mark.django_db


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Test Septic")


@pytest.fixture
def user(db):
    return User.objects.create_superuser("owner", "owner@example.com", "pw12345!!")


@pytest.fixture
def client(client: Client, user: User) -> Client:
    client.force_login(user)
    return client


def _complete(org: Organization, customer: Customer, day: datetime.date, gallons: int) -> Job:
    """Route one stop and close it out through the real completion path."""
    job = Job.objects.create(organization=org, customer=customer, route_day=day)
    job.mark_completed(
        gallons=gallons,
        disposal_site="North WWTP",
        completion_notes=f"routine {day.isoformat()}",
        pumped_on=day,
    )
    return job


class TestLedgerOnCompletion:
    def test_mark_completed_appends_tank_event(self, org: Organization):
        customer = Customer.objects.create(
            organization=org,
            name="Doe Residence",
            address="1 Main St",
            parcel_id="MAP 17 LOT 12",
            tank_size_gallons=1000,
            pump_interval_months=12,
        )
        day = datetime.date(2026, 3, 2)

        _complete(org, customer, day, gallons=900)

        ledger = list(customer.tank_ledger)
        assert len(ledger) == 1
        event = ledger[0]
        assert event.event_date == day
        assert event.gallons == 900
        assert event.disposal_site == "North WWTP"
        assert event.source == TankEventSource.JOB_COMPLETION
        assert event.job is not None
        customer.refresh_from_db()
        assert customer.last_pumped == day
        assert customer.next_due == datetime.date(2027, 3, 2)

    def test_repeat_visits_accumulate_instead_of_overwriting(self, org: Organization):
        customer = Customer.objects.create(organization=org, name="Diner", address="9 Elm St")

        _complete(org, customer, datetime.date(2025, 3, 2), gallons=800)
        _complete(org, customer, datetime.date(2026, 3, 2), gallons=850)

        assert customer.tank_ledger.count() == 2
        newest = customer.tank_ledger.first()
        assert newest is not None
        assert newest.event_date == datetime.date(2026, 3, 2)


class TestParcelGrouping:
    def test_history_follows_the_tank_across_accounts(self, org: Organization):
        seller = Customer.objects.create(
            organization=org, name="Prior Owner", address="12 Maple St", parcel_id="map17-lot12"
        )
        successor = Customer.objects.create(
            organization=org, name="New Owner", address="12 Maple St", parcel_id="MAP17-LOT12"
        )
        stranger = Customer.objects.create(
            organization=org, name="Down The Road", address="14 Maple St", parcel_id="map17-lot13"
        )

        _complete(org, seller, datetime.date(2024, 6, 1), gallons=700)

        assert seller.tank_key == successor.tank_key
        assert seller.tank_key != stranger.tank_key
        successor_events = list(successor.tank_ledger)
        assert [event.customer_id for event in successor_events] == [seller.pk]
        assert stranger.tank_ledger.count() == 0

    def test_address_fallback_groups_when_parcel_unknown(self, org: Organization):
        first = Customer.objects.create(
            organization=org, name="Cottage A", address="7 Shore Rd", city="", zip_code="01095"
        )
        reimported = Customer.objects.create(
            organization=org,
            name="Shore Rd Cottage",
            address="7 Shore Rd",
            city="",
            zip_code="01095",
        )
        elsewhere = Customer.objects.create(
            organization=org, name="Bungalow", address="8 Shore Rd", city="", zip_code="01095"
        )

        _complete(org, first, datetime.date(2025, 5, 5), gallons=500)

        assert first.tank_key == reimported.tank_key
        assert reimported.tank_ledger.count() == 1
        assert elsewhere.tank_ledger.count() == 0

    def test_from_import_row_still_builds_address_keyed_customers(self, org: Organization):
        row = CustomerRow(
            name="Imported Shop",
            address="3 Bay St",
            last_pumped=datetime.date(2023, 1, 15),
            pump_interval_months=36,
        )

        customer = Customer.from_import_row(org, row)

        assert customer.next_due == datetime.date(2026, 1, 15)
        assert customer.parcel_id == ""
        assert customer.tank_key == "addr:3 bay st||"


class TestRouteSaleExport:
    def test_zip_contains_expected_ledger_and_due_rows(self, client: Client, org: Organization):
        pumped = Customer.objects.create(
            organization=org,
            name="Pumped Shop",
            address="1 Main St",
            parcel_id="P1",
            tank_size_gallons=1000,
            pump_interval_months=12,
        )
        never = "Never Pumped"  # asserted by absence from due_dates.csv below
        Customer.objects.create(organization=org, name=never, address="2 Elm St")
        _complete(org, pumped, datetime.date(2026, 1, 10), gallons=900)
        TankEvent.objects.create(
            customer=pumped,
            event_date=datetime.date(2026, 1, 20),
            gallons=50,
            source=TankEventSource.MANUAL_ENTRY,
        )
        as_of = datetime.date(2026, 1, 15)

        response = client.get(reverse("route_sale_export", args=[as_of.isoformat()]))

        assert response.status_code == 200
        assert response["Content-Type"] == "application/zip"
        assert "route-sale-2026-01-15.zip" in response["Content-Disposition"]
        bundle = zipfile.ZipFile(io.BytesIO(response.content))
        assert set(bundle.namelist()) == {"tank_ledger.csv", "due_dates.csv"}

        ledger_rows = list(csv.reader(io.StringIO(bundle.read("tank_ledger.csv").decode())))
        assert ledger_rows[0][:7] == [
            "customer",
            "address",
            "city",
            "state",
            "zip",
            "parcel_id",
            "event_date",
        ]
        # Only the on-or-before-as-of event exports; the Jan 20 entry stays out.
        assert [(row[0], row[6], row[7]) for row in ledger_rows[1:]] == [
            ("Pumped Shop", "2026-01-10", "900")
        ]

        due_rows = list(csv.reader(io.StringIO(bundle.read("due_dates.csv").decode())))
        assert due_rows[0] == [
            "customer",
            "address",
            "parcel_id",
            "tank_size_gallons",
            "last_pumped",
            "pump_interval_months",
            "next_due",
        ]
        # Never-pumped accounts carry no due date, so only one data row.
        assert [row[0] for row in due_rows[1:]] == ["Pumped Shop"]
        assert due_rows[1][6] == "2027-01-10"

    def test_bad_date_returns_404(self, client: Client):
        response = client.get(reverse("route_sale_export", args=["not-a-date"]))

        assert response.status_code == 404


class TestDataGravity:
    def test_tenure_compounds_into_records_a_departing_shop_abandons(
        self, client: Client, org: Organization
    ):
        """The churn lever, asserted: each serviced year deepens the ledger.

        A rival can copy a customer list in an afternoon; three years of
        gallon-by-gallon disposal history lives only here. Leaving means
        abandoning the balance sheet, so staying is the cheap option.
        """
        customer = Customer.objects.create(
            organization=org,
            name="Loyal Account",
            address="45 Main St",
            parcel_id="MAP 09 LOT 41",
            pump_interval_months=12,
        )
        for year, gallons in ((2024, 980), (2025, 1010), (2026, 1040)):
            _complete(org, customer, datetime.date(year, 4, 1), gallons=gallons)

        assert customer.tank_ledger.count() == 3

        as_of = datetime.date(2026, 12, 31)
        response = client.get(reverse("route_sale_export", args=[as_of.isoformat()]))
        bundle = zipfile.ZipFile(io.BytesIO(response.content))
        ledger_csv = bundle.read("tank_ledger.csv").decode()

        for year in (2024, 2025, 2026):
            assert f"{year}-04-01" in ledger_csv
        assert "Loyal Account" in ledger_csv
