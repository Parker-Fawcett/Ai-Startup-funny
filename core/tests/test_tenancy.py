"""Multi-tenant isolation: each owner sees only their own shop's book."""

import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.models import Customer, Job, Organization

pytestmark = pytest.mark.django_db


@pytest.fixture
def two_shops():
    owner_a = User.objects.create_superuser("a", "a@x.co", "pw12345!!")
    owner_b = User.objects.create_superuser("b", "b@x.co", "pw12345!!")
    org_a = Organization.objects.create(name="Shop A", owner=owner_a)
    org_b = Organization.objects.create(name="Shop B", owner=owner_b)
    ca = Customer.objects.create(organization=org_a, name="A-customer", address="1")
    cb = Customer.objects.create(organization=org_b, name="B-customer", address="2")
    return org_a, org_b, ca, cb, owner_a, owner_b


def test_owner_sees_only_own_customers_on_route(client: Client, two_shops):
    _, _, _, _, _, owner_b = two_shops
    c = Client()
    c.force_login(owner_b)

    body = c.get(reverse("route_day", args=[datetime.date.today().isoformat()])).content.decode()

    assert "B-customer" in body
    assert "A-customer" not in body


def test_signup_links_new_org_to_its_owner():
    payload = {
        "shop_name": "Linked Co",
        "email": "link@x.co",
        "password1": "Sturdy!Pass99",
        "password2": "Sturdy!Pass99",
        "website": "",
    }
    Client().post(reverse("signup"), payload)

    assert Organization.objects.get(name="Linked Co").owner.username == "link@x.co"


class TestRebuildSafety:
    def test_reselecting_completed_customer_does_not_crash(self, client: Client, two_shops):
        """The demo-day bug: re-POSTing a stop already completed today must not 500."""
        org_a, _, ca, _, owner_a, _ = two_shops
        Job.objects.create(
            organization=org_a,
            customer=ca,
            route_day=datetime.date.today(),
            status="completed",
            gallons=900,
        )
        c = Client()
        c.force_login(owner_a)

        response = c.post(
            reverse("route_day", args=[datetime.date.today().isoformat()]),
            {"customers": [str(ca.pk)], "driver": "Ray"},
        )

        assert response.status_code == 302
