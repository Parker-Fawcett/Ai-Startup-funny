import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.models import Customer, Job, JobStatus, Organization

pytestmark = pytest.mark.django_db


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Test Septic", home_lat=42.101, home_lng=-72.589)


@pytest.fixture
def client(client: Client, user: User) -> Client:
    client.force_login(user)
    return client


@pytest.fixture
def user(db):
    return User.objects.create_superuser("owner", "owner@example.com", "pw12345!!")


class TestDashboard:
    def test_buckets_overdue_due30_due90(self, client: Client, org: Organization):
        today = datetime.date.today()
        Customer.objects.create(
            organization=org,
            name="Old",
            address="a",
            last_pumped=today - datetime.timedelta(days=400),
            pump_interval_months=12,
        )
        Customer.objects.create(
            organization=org,
            name="Soon",
            address="b",
            last_pumped=today - datetime.timedelta(days=350),
            pump_interval_months=12,
        )
        Customer.objects.create(
            organization=org,
            name="Mid",
            address="c",
            last_pumped=today - datetime.timedelta(days=300),
            pump_interval_months=12,
        )
        Customer.objects.create(
            organization=org, name="Fine", address="d", last_pumped=today, pump_interval_months=12
        )

        response = client.get(reverse("dashboard"))

        assert response.status_code == 200
        body = response.content.decode()
        assert "Old" in body
        assert "Soon" in body
        assert "Mid" in body
        assert "Fine" not in body


class TestImportView:
    def test_get_renders_form(self, client: Client):
        response = client.get(reverse("import"))

        assert response.status_code == 200

    def test_post_creates_customers_from_csv(self, client: Client, org: Organization):
        csv_text = (
            "name,address,city,state,zip,tank_size_gallons,pump_interval_months,last_pumped\n"
            f"Doe Residence,1 Main St,Springfield,MA,01101,1000,36,{datetime.date.today() - datetime.timedelta(days=370)}\n"
            "Corner Diner,9 Elm St,Springfield,MA,01102,,,\n"
        ).encode()

        response = client.post(reverse("import"), {"csv_file": __import__("io").BytesIO(csv_text)})

        assert response.status_code == 302
        assert org.customers.count() == 2
        doe = org.customers.get(name="Doe Residence")
        assert doe.tank_size_gallons == 1000
        assert doe.next_due is not None

    def test_post_with_errors_reports_and_imports_valid_rows(
        self, client: Client, org: Organization
    ):
        csv_text = b"name,address\nGood Shop,5 Rd\n,No Name Ln\n"

        response = client.post(reverse("import"), {"csv_file": __import__("io").BytesIO(csv_text)})

        assert response.status_code == 200
        assert org.customers.count() == 1
        assert "row 3" in response.content.decode().lower()


class TestRouteDay:
    def test_post_builds_jobs_in_nearest_neighbor_order(self, client: Client, org: Organization):
        near = Customer.objects.create(
            organization=org, name="Near", address="a", lat=42.102, lng=-72.590
        )
        far = Customer.objects.create(
            organization=org, name="Far", address="b", lat=42.250, lng=-72.900
        )
        mid = Customer.objects.create(
            organization=org, name="Mid", address="c", lat=42.150, lng=-72.700
        )
        day = datetime.date.today()

        response = client.post(
            reverse("route_day", args=[day.isoformat()]),
            {"customers": [str(far.pk), str(near.pk), str(mid.pk)]},
        )

        assert response.status_code == 302
        jobs = Job.objects.filter(route_day=day).order_by("position")
        assert [j.customer_id for j in jobs] == [near.pk, mid.pk, far.pk]

    def test_rebuild_replaces_previous_pending_jobs(self, client: Client, org: Organization):
        one = Customer.objects.create(
            organization=org, name="One", address="a", lat=42.0, lng=-72.0
        )
        two = Customer.objects.create(
            organization=org, name="Two", address="b", lat=42.2, lng=-72.4
        )
        day = datetime.date.today()
        client.post(reverse("route_day", args=[day.isoformat()]), {"customers": [str(one.pk)]})

        client.post(reverse("route_day", args=[day.isoformat()]), {"customers": [str(two.pk)]})

        jobs = Job.objects.filter(route_day=day)
        assert jobs.count() == 1
        assert jobs.first().customer_id == two.pk

    def test_completed_jobs_survive_rebuild(self, client: Client, org: Organization):
        one = Customer.objects.create(
            organization=org, name="One", address="a", lat=42.0, lng=-72.0
        )
        day = datetime.date.today()
        client.post(reverse("route_day", args=[day.isoformat()]), {"customers": [str(one.pk)]})
        job = Job.objects.get(route_day=day)
        job.status = JobStatus.COMPLETED
        job.save()

        other = Customer.objects.create(
            organization=org, name="Two", address="b", lat=42.2, lng=-72.4
        )
        client.post(reverse("route_day", args=[day.isoformat()]), {"customers": [str(other.pk)]})

        statuses = {j.customer_id: j.status for j in Job.objects.filter(route_day=day)}
        assert statuses == {one.pk: JobStatus.COMPLETED, other.pk: JobStatus.PENDING}


class TestJobComplete:
    def test_post_completes_job_and_rolls_cycle(self, client: Client, org: Organization):
        customer = Customer.objects.create(
            organization=org,
            name="C",
            address="a",
            last_pumped=datetime.date(2020, 1, 15),
            pump_interval_months=12,
        )
        day = datetime.date.today()
        job = Job.objects.create(organization=org, customer=customer, route_day=day)

        response = client.post(
            reverse("job_complete", args=[job.pk]),
            {"gallons": "1250", "disposal_site": "North WWTP", "notes": "clean lid"},
        )

        assert response.status_code == 302
        job.refresh_from_db()
        customer.refresh_from_db()
        assert job.status == JobStatus.COMPLETED
        assert job.gallons == 1250
        assert customer.last_pumped == day
        assert customer.next_due == day + datetime.timedelta(days=365)


class TestJobReportPdf:
    def test_returns_pdf_bytes_with_disclaimer(self, client: Client, org: Organization):
        customer = Customer.objects.create(
            organization=org, name="Report Buyer", address="10 Station Rd"
        )
        job = Job.objects.create(
            organization=org,
            customer=customer,
            route_day=datetime.date.today(),
            status=JobStatus.COMPLETED,
            gallons=900,
            disposal_site="North WWTP",
        )

        response = client.get(reverse("job_report", args=[job.pk]))

        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        body = response.content
        assert body.startswith(b"%PDF")
        assert b"not legal advice" in body.lower()
