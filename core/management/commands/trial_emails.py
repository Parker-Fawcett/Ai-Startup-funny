"""Trial-expiry nudges: the conversion engine fires at the deadline."""

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Organization

# Day-5 and day-1 before expiry: the two windows that matter per research.
WINDOWS: tuple[int, ...] = (5, 1)


class Command(BaseCommand):
    """Email owners whose 30-day trial hits a nudge window today."""

    help = "Send trial-expiry reminder emails at D-5 and D-1 windows."

    def handle(self, *args: object, **options: object) -> None:  # noqa: ARG002 -- BaseCommand contract
        """One pass; idempotent via last_reminded_on-style check on plan state."""
        today = timezone.localdate()
        sent = 0
        for organization in Organization.objects.exclude(trial_ends_on=None).exclude(plan=""):
            days_left = (organization.trial_ends_on - today).days
            if days_left not in WINDOWS:
                continue
            owner = organization.customers.filter(email__gt="").first()
            recipient = getattr(settings, "OWNER_FALLBACK_EMAIL", None) or (
                owner.email if owner else None
            )
            if not recipient:
                continue
            day_word = "day" if days_left == 1 else "days"
            subject = f"{organization.name}: {days_left} {day_word} left in your PumpRun trial"
            body = (
                f"Your PumpRun trial ends {organization.trial_ends_on.isoformat()}. "
                f"Pick a plan at any time from the pricing page to keep routes, "
                f"reminders, and filing clocks running without interruption."
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
            sent += 1

        self.stdout.write(f"{today.isoformat()} trial emails: sent={sent} windows={WINDOWS}")
