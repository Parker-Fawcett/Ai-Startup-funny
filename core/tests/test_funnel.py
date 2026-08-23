"""Funnel instrumentation: four conversion events recorded and queryable."""

import datetime

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from core.funnel import track
from core.models import Customer, FunnelEvent, Job, Organization

pytestmark = pytest.mark.django_db


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Funnel Shop")


class TestTrack:
    def test_event_stored_with_org_and_meta(self, org):
        track("import_completed", organization=org, rows=7)

        event = FunnelEvent.objects.get()
        assert event.name == "import_completed"
        assert event.organization == org
        assert event.meta["rows"] == 7

    def test_anonymous_event_allowed(self):
        track("visited_pricing")

        assert FunnelEvent.objects.get().organization is None

    def test_unknown_name_rejected(self):
        with pytest.raises(ValidationError):
            track("made_up_event")


class TestWiredSurfaces:
    def test_pricing_visit_tracked(self):
        Client().get(reverse("pricing"))

        assert FunnelEvent.objects.filter(name="visited_pricing").exists()

    def test_signup_created_tracked(self):
        payload = {
            "shop_name": "Track Co",
            "email": "t@track.co",
            "password1": "Sturdy!Pass99",
            "password2": "Sturdy!Pass99",
            "website": "",
        }
        Client().post(reverse("signup"), payload)

        event = FunnelEvent.objects.get(name="signup_created")
        assert event.organization.name == "Track Co"

    def test_import_completed_carries_row_count(self, client, org):
        customer = Customer.objects.create(organization=org, name="x", address="y")
        job = Job.objects.create(
            organization=org, customer=customer, route_day=datetime.date.today()
        )
        _ = job  # org context only

        csv_text = (
            f"name,address,tank_size_gallons,last_pumped\n"
            f"A,1 Rd,1000,{datetime.date.today() - datetime.timedelta(days=370)}\n"
            f"B,2 Rd,,\n"
        ).encode()
        c = Client()
        u = User.objects.create_superuser("fx", "fx@x.co", "pw12345!!")
        c.force_login(u)
        c.post(reverse("import"), {"csv_file": SimpleUploadedFile("b.csv", csv_text)})

        event = FunnelEvent.objects.filter(name="import_completed").get()
        assert event.meta["rows"] == 2
