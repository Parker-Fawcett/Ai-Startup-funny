import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from core.models import Customer, Job, JobStatus, Organization


@pytest.mark.django_db
class TestCustomerDueDate:
    def test_stores_next_due_from_last_pumped_and_interval(self):
        org = Organization.objects.create(name="Test Septic")

        customer = Customer.objects.create(
            organization=org,
            name="Doe Residence",
            address="1 Main St",
            last_pumped=datetime.date(2026, 1, 15),
            pump_interval_months=36,
        )

        assert customer.next_due == datetime.date(2029, 1, 15)

    def test_recomputes_next_due_when_last_pumped_updates(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(
            organization=org,
            name="Doe Residence",
            address="1 Main St",
            last_pumped=datetime.date(2020, 1, 31),
            pump_interval_months=1,
        )

        customer.last_pumped = datetime.date(2024, 1, 31)
        customer.save()

        assert customer.next_due == datetime.date(2024, 2, 29)

    def test_next_due_is_none_while_never_pumped(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(
            organization=org,
            name="New Install",
            address="2 Elm St",
            pump_interval_months=36,
        )

        assert customer.next_due is None

    def test_coords_none_until_geocoded(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(organization=org, name="No Geo", address="3 Oak St")

        assert customer.coords is None

    def test_coords_pair_once_geocoded(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(
            organization=org,
            name="Geocoded",
            address="4 Pine St",
            lat=42.1,
            lng=-71.5,
        )

        assert customer.coords == (42.1, -71.5)


@pytest.mark.django_db
class TestJob:
    def test_new_job_defaults_to_pending(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(organization=org, name="C", address="a")

        job = Job.objects.create(
            organization=org, customer=customer, route_day=datetime.date(2026, 3, 2)
        )

        assert job.status == JobStatus.PENDING
        assert job.completed_at is None

    def test_same_customer_twice_same_day_is_rejected(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(organization=org, name="C", address="a")
        day = datetime.date(2026, 3, 2)
        Job.objects.create(organization=org, customer=customer, route_day=day)

        duplicate = Job(organization=org, customer=customer, route_day=day)

        with pytest.raises(IntegrityError):
            duplicate.save()

    def test_status_transition_records_report_fields(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(organization=org, name="C", address="a")
        job = Job.objects.create(
            organization=org,
            customer=customer,
            route_day=datetime.date(2026, 3, 2),
            gallons=1000,
            disposal_site="North WWTP",
        )

        job.status = JobStatus.COMPLETED
        job.completed_at = timezone.now()
        job.save()

        job.refresh_from_db()
        assert job.status == JobStatus.COMPLETED
        assert job.gallons == 1000
        assert job.disposal_site == "North WWTP"

    def test_invalid_status_rejected_by_choices(self):
        org = Organization.objects.create(name="Test Septic")
        customer = Customer.objects.create(organization=org, name="C", address="a")
        job = Job(
            organization=org,
            customer=customer,
            route_day=datetime.date(2026, 3, 2),
            status="teleported",
        )

        with pytest.raises(ValidationError):
            job.full_clean()
