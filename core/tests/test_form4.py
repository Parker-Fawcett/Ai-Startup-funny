"""Form 4 capture, photo attachments, and route-driver assignment."""

import datetime

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from core.models import Customer, Job, Organization

pytestmark = pytest.mark.django_db


@pytest.fixture
def org():
    return Organization.objects.create(name="Test Septic")


@pytest.fixture
def client(client: Client, user):
    return client


def _make_customer_job(org, tank=1000):
    customer = Customer.objects.create(
        organization=org, name="Ledger Buyer", address="1 Rd", tank_size_gallons=tank
    )
    job = Job.objects.create(organization=org, customer=customer, route_day=datetime.date.today())
    return customer, job


class TestForm4FieldsAndPhotos:
    def test_filter_and_system_type_persist_on_completion(self, client, org):
        _, job = _make_customer_job(org)

        response = client.post(
            reverse("job_complete", args=[job.pk]),
            {
                "gallons": "800",
                "disposal_site": "North WWTP",
                "notes": "",
                "filter_action": "replaced",
                "system_type": "Septic tank",
            },
        )

        assert response.status_code == 302
        job.refresh_from_db()
        job.customer.refresh_from_db()
        assert job.filter_action == "replaced"
        assert job.customer.system_type == "Septic tank"

    def test_photo_attachment_saved_with_job(self, client, org):
        _, job = _make_customer_job(org)
        photo = SimpleUploadedFile(
            "tank.jpg", b"\xff\xd8\xff\xe0fakejpg", content_type="image/jpeg"
        )

        response = client.post(
            reverse("job_complete", args=[job.pk]),
            {
                "gallons": "800",
                "disposal_site": "North WWTP",
                "notes": "",
                "filter_action": "cleaned",
                "photo": photo,
            },
        )

        assert response.status_code == 302
        attachment = job.attachments.get()
        assert attachment.file.name.endswith("tank.jpg")
        attachment.file.delete(save=False)
        attachment.delete()

    def test_non_photo_extension_rejected(self, client, org):
        _, job = _make_customer_job(org)
        payload = SimpleUploadedFile("evil.exe", b"MZ", content_type="application/x-msdownload")

        response = client.post(
            reverse("job_complete", args=[job.pk]),
            {
                "gallons": "800",
                "disposal_site": "North WWTP",
                "notes": "",
                "filter_action": "none",
                "photo": payload,
            },
        )

        assert response.status_code == 200
        assert not Job.objects.get(pk=job.pk).attachments.exists()

    def test_pdf_includes_form4_rows(self, client, org):
        customer = Customer.objects.create(
            organization=org, name="PDF Buyer", address="9 Rd", system_type="Septic tank"
        )
        job = Job.objects.create(
            organization=org, customer=customer, route_day=datetime.date.today()
        )
        job.mark_completed(
            gallons=900,
            disposal_site="North WWTP",
            completion_notes="",
            pumped_on=datetime.date.today(),
            filter_action="cleaned",
        )

        response = client.get(reverse("job_report", args=[job.pk]))

        body = response.content
        assert b"ilter service" in body
        assert b"leaned" in body
        assert b"ystem type" in body
        assert b"eptic tank" in body


class TestRouteDriver:
    def test_post_with_driver_stamps_jobs(self, client, org):
        near = Customer.objects.create(
            organization=org, name="Near", address="a", lat=42.1, lng=-72.6
        )
        day = datetime.date.today()

        response = client.post(
            reverse("route_day", args=[day.isoformat()]),
            {"customers": [str(near.pk)], "driver": "Ray"},
        )

        assert response.status_code == 302
        job = org.jobs.get(route_day=day)
        assert job.driver == "Ray"
