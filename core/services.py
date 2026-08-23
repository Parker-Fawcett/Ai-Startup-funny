"""Application service layer: operations views shouldn't hand-roll."""

import datetime
from collections.abc import Sequence

from core.models import Customer, Job, JobStatus, Organization
from core.routing import GeoPoint, LatLng, nearest_neighbor_order


def get_default_organization() -> Organization:
    """Bootstrap-mode single-shop fallback; prefer ``for_user`` when authed."""
    organization = Organization.objects.first()
    if organization is None:
        organization = Organization.objects.create(name="My Septic")
    return organization


def get_organization_for_user(user: object) -> Organization:
    """Resolve the signed-in owner's shop; falls back to the bootstrap row."""
    from django.contrib.auth.models import AnonymousUser  # noqa: PLC0415 -- typing aid only

    if not isinstance(user, AnonymousUser) and getattr(user, "is_authenticated", False):
        owned = user.organizations.order_by("pk").first()
        if owned is not None:
            return owned
    return get_default_organization()


def build_route(
    organization: Organization,
    route_day: datetime.date,
    customer_ids: Sequence[int],
    driver: str = "",
) -> list[Job]:
    """Replace the day's pending jobs with a nearest-neighbor-ordered plan.

    Customers without coordinates keep input order at the tail of the route.
    Completed/skipped jobs for the day are never touched.
    """
    selected = {
        customer.pk: customer
        for customer in Customer.objects.filter(organization=organization, pk__in=set(customer_ids))
    }
    kept_ids = [pk for pk in customer_ids if pk in selected]
    geocoded = [selected[pk] for pk in kept_ids if selected[pk].coords is not None]
    ungeocoded = [selected[pk] for pk in kept_ids if selected[pk].coords is None]

    start: LatLng | None = None
    if organization.home_coords is not None:
        start = organization.home_coords
    elif geocoded:
        start = geocoded[0].coords

    ordered: list[Customer] = []
    if start is not None and geocoded:
        points = [
            GeoPoint(stop_id=customer.pk, lat=customer.lat, lng=customer.lng)
            for customer in geocoded
        ]
        visit_order = nearest_neighbor_order(start, points)
        ordered = [selected[pk] for pk in visit_order] + ungeocoded
    else:
        ordered = ungeocoded

    Job.objects.filter(
        organization=organization, route_day=route_day, status=JobStatus.PENDING
    ).delete()

    already_today = set(
        Job.objects.filter(
            organization=organization,
            route_day=route_day,
            status__in=(JobStatus.COMPLETED, JobStatus.SKIPPED),
        ).values_list("customer_id", flat=True)
    )
    ordered = [c for c in ordered if c.pk not in already_today]

    jobs = [
        Job(
            organization=organization,
            customer=customer,
            route_day=route_day,
            position=index + 1,
            driver=driver,
        )
        for index, customer in enumerate(ordered)
    ]
    Job.objects.bulk_create(jobs)
    return list(Job.objects.filter(organization=organization, route_day=route_day))
