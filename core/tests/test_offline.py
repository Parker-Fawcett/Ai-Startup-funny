"""Offline PWA plumbing: guard against replay double-books, assets served."""

import datetime
import pathlib

import pytest
from django.contrib.staticfiles import finders
from django.test import Client
from django.urls import reverse

from core.models import Customer, Invoice, Job, Organization, TankEvent

pytestmark = pytest.mark.django_db


@pytest.fixture
def org():
    return Organization.objects.create(name="Test Septic")


@pytest.fixture
def client(client: Client, user):
    return client


def _completed_job(org) -> tuple[Job, Customer]:
    customer = Customer.objects.create(
        organization=org,
        name="Replay",
        address="1 Rd",
        tank_size_gallons=1000,
        last_pumped=datetime.date(2023, 1, 1),
        pump_interval_months=36,
    )
    job = Job.objects.create(organization=org, customer=customer, route_day=datetime.date.today())
    job.mark_completed(
        gallons=800, disposal_site="x", completion_notes="", pumped_on=datetime.date.today()
    )
    return job, customer


class TestReplayGuard:
    def test_second_post_is_noop_with_notice(self, client, org):
        job, _ = _completed_job(org)
        before_events = TankEvent.objects.count()
        before_invoices = Invoice.objects.count()
        customer = job.customer
        last_pumped_before = customer.last_pumped

        response = client.post(
            reverse("job_complete", args=[job.pk]),
            {"gallons": "9999", "disposal_site": "evil", "notes": "", "filter_action": "none"},
            follow=True,
        )

        assert response.status_code == 200
        assert b"already closed" in response.content
        job.refresh_from_db()
        assert job.gallons == 800  # untouched
        assert customer.last_pumped == last_pumped_before  # cycle not re-rolled
        assert TankEvent.objects.count() == before_events
        assert Invoice.objects.count() == before_invoices

    def test_replay_after_offline_style_resubmission_keeps_single_invoice(self, client, org):
        job, _ = _completed_job(org)

        client.post(
            reverse("job_complete", args=[job.pk]),
            {"gallons": "700", "disposal_site": "y", "notes": ""},
        )
        client.post(
            reverse("job_complete", args=[job.pk]),
            {"gallons": "600", "disposal_site": "z", "notes": ""},
        )

        assert Invoice.objects.filter(job=job).count() == 1
        assert TankEvent.objects.filter(job=job).count() == 1


def _asset(name: str) -> bytes:
    found = finders.find(f"pumprun/{name}")
    assert found is not None
    return pathlib.Path(str(found)).read_bytes()


class TestOfflineAssets:
    def test_service_worker_ships_replay_logic(self):
        body = _asset("sw.js")
        assert b"pumprun-replay" in body
        assert b"indexedDB" in body

    def test_manifest_is_installable_pwa(self):
        body = _asset("manifest.webmanifest")
        assert b'"name": "PumpRun"' in body
        assert b'"display": "standalone"' in body

    def test_base_template_registers_pwa(self, client, user):
        client.force_login(user)
        body = client.get(reverse("dashboard")).content
        assert b"manifest.webmanifest" in body
        assert b"offline.js" in body

    def test_complete_form_marked_for_queue(self, client, org):
        customer = Customer.objects.create(organization=org, name="Q", address="r")
        job = Job.objects.create(
            organization=org, customer=customer, route_day=datetime.date.today()
        )

        body = client.get(reverse("job_complete", args=[job.pk])).content

        assert b"data-offline-queue" in body


class TestBranded404:
    def test_404_renders_branded_page(self, settings):
        from django.test import Client

        settings.DEBUG = False
        response = Client().get("/this-page-does-not-exist/")
        assert response.status_code == 404
        body = response.content.decode()
        assert "isn&#x27;t on the route" in body or "isn't on the route" in body
        assert "PumpRun" in body
