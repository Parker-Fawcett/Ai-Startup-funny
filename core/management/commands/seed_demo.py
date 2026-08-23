"""Seed a demo shop with customers and today's route."""

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Customer, Job, Organization
from core.services import build_route


class Command(BaseCommand):
    """Management command seeding demo data."""

    help = "Seed demo organization, customers, and today's route."

    def handle(self, *args: object, **options: object) -> None:
        """Create the demo organization, customers, route, and one completion."""
        if Organization.objects.exists():
            self.stdout.write("Organization already exists; skipping seed.")
            return

        org = Organization.objects.create(
            name="Pioneer Valley Septic", home_lat=42.1015, home_lng=-72.5898
        )
        today = timezone.localdate()

        def days_ago(n: int) -> datetime.date:
            return today - datetime.timedelta(days=n)

        demo = [
            ("Doe Residence", "12 Maple St, Springfield", 42.1102, -72.5901, 1000, 12, 400),
            ("Corner Diner", "9 Elm St, Springfield", 42.1210, -72.6102, 1500, 6, 170),
            ("Springfield Elementary", "45 Main St", 42.0950, -72.5754, 2000, 6, 160),
            ("Riverside Church", "3 Bay St", 42.1051, -72.5997, 1250, 12, 355),
            ("Highland Auto", "88 Highland Ave", 42.1320, -72.6400, 1000, 12, 340),
            ("Maplewood Apartments", "21 Oak St", 42.1088, -72.6050, 3000, 6, 150),
            ("Bayside Cottage", "7 Shore Rd, Wilbraham", 42.1107, -72.4980, 750, 36, 100),
            ("Old Mill Bistro", "40 Mill Ln, Chicopee", 42.1487, -72.6079, 1750, 6, 155),
        ]
        for name, address, lat, lng, gallons, interval, ago in demo:
            Customer.objects.create(
                organization=org,
                name=name,
                address=address,
                city="",
                state="MA",
                zip_code="",
                lat=lat,
                lng=lng,
                tank_size_gallons=gallons,
                pump_interval_months=interval,
                last_pumped=days_ago(ago),
            )

        due_ids = list(
            org.customers.filter(next_due__lte=timezone.localdate()).values_list("pk", flat=True)[
                :5
            ]
        )
        build_route(org, timezone.localdate(), due_ids)

        org.customers.filter(name="Corner Diner").update(
            email="diner@example.com", phone="+14135550111"
        )
        org.customers.filter(name="Doe Residence").update(email="doe@example.com")

        first_job = Job.objects.filter(route_day=timezone.localdate()).order_by("position").first()
        if first_job:
            first_job.mark_completed(
                gallons=1020,
                disposal_site="Springfield Regional WWTP",
                completion_notes="Routine pump-out; baffle intact.",
                pumped_on=timezone.localdate(),
            )

        self.stdout.write(
            f"Seeded Pioneer Valley Septic: {org.customers.count()} customers, "
            f"{Job.objects.count()} jobs on today's route."
        )
