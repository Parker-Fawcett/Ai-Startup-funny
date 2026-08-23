"""Email/SMS pump-due reminders; cron/beat this daily, run by hand anytime."""

import argparse

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from core import sms as sms_channel
from core.models import Customer
from core.reminders import (
    DEFAULT_MIN_RESEND_DAYS,
    DEFAULT_WINDOW_DAYS,
    decide,
    render_reminder,
    render_sms,
)

_CHANNELS = ("email", "sms", "both")


class Command(BaseCommand):
    """Send due-soon/overdue pumping reminders over the chosen channel(s)."""

    help = "Email/SMS pump-due reminders; stamps last_reminded_on per customer."

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Expose channel, window, resend guard, and dry-run knobs."""
        parser.add_argument("--channel", choices=_CHANNELS, default="email")
        parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
        parser.add_argument("--min-resend-days", type=int, default=DEFAULT_MIN_RESEND_DAYS)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args: object, **options: object) -> None:  # noqa: ARG002 -- BaseCommand contract
        """Decide per customer, deliver on the channel(s), stamp, summarize."""
        today = timezone.localdate()
        channel: str = options["channel"]  # type: ignore[assignment]
        window_days: int = options["window_days"]  # type: ignore[assignment]
        min_resend_days: int = options["min_resend_days"]  # type: ignore[assignment]
        dry_run: bool = options["dry_run"]  # type: ignore[assignment]

        use_email = channel in ("email", "both")
        use_sms = channel in ("sms", "both")
        if use_sms and not (dry_run or sms_channel.enabled()):
            self.stdout.write("SMS requested but TWILIO_* settings are missing — nothing sent.")
            return

        sent, skipped, failures = 0, {}, 0
        for customer in Customer.objects.exclude(next_due=None):
            decision = decide(
                next_due=customer.next_due,
                today=today,
                last_reminded_on=customer.last_reminded_on,
                window_days=window_days,
                min_resend_days=min_resend_days,
            )
            if not decision.should_send:
                skipped[decision.reason] = skipped.get(decision.reason, 0) + 1
                continue

            subject, body = render_reminder(
                customer_name=customer.name,
                org_name=customer.organization.name,
                next_due=customer.next_due,
                today=today,
            )
            text_message = render_sms(
                org_name=customer.organization.name,
                next_due=customer.next_due,
                today=today,
            )
            delivered = self._send_all_channels(
                customer,
                use_email=use_email,
                use_sms=use_sms,
                subject=subject,
                body=body,
                text_message=text_message,
                dry_run=dry_run,
                skipped=skipped,
            )
            if delivered:
                sent += 1
                if not dry_run:
                    customer.last_reminded_on = today
                    customer.save(update_fields=["last_reminded_on"])

        self.stdout.write(
            f"{today.isoformat()} reminders[{channel}]: sent={sent} skipped={skipped} "
            f"failures={failures} (window={window_days}d resend>={min_resend_days}d "
            f"dry_run={dry_run})"
        )

    def _send_all_channels(  # noqa: PLR0913 -- per-channel context beats a params blob
        self,
        customer: Customer,
        *,
        use_email: bool,
        use_sms: bool,
        subject: str,
        body: str,
        text_message: str,
        dry_run: bool,
        skipped: dict[str, int],
    ) -> bool:
        """Deliver on every applicable channel; True once anything lands."""
        delivered = False
        if use_email:
            if customer.email:
                delivered = self._email(customer.email, subject, body, dry_run=dry_run)
            else:
                self._skip(skipped, "no_email")

        if use_sms:
            if customer.sms_opt_out:
                self._skip(skipped, "sms_opt_out")
            elif not customer.phone:
                self._skip(skipped, "no_phone")
            else:
                delivered = self._sms(customer.phone, text_message, dry_run=dry_run) or delivered
        return delivered

    def _email(self, to: str, subject: str, body: str, *, dry_run: bool) -> bool:
        if dry_run:
            self.stdout.write(f"[dry] email -> {to}: {subject}")
            return True
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to])
        except Exception as error:  # noqa: BLE001 -- one bad address must not kill the batch
            self.stderr.write(f"FAILED email {to}: {error}")
            return False
        return True

    def _sms(self, to: str, text_message: str, *, dry_run: bool) -> bool:
        if dry_run:
            self.stdout.write(f"[dry] sms -> {to}: {text_message}")
            return True
        try:
            sms_channel.send_sms(to, text_message)
        except sms_channel.SmsError as error:
            self.stderr.write(f"FAILED sms {to}: {error}")
            return False
        return True

    def _skip(self, skipped: dict[str, int], reason: str) -> None:
        skipped[reason] = skipped.get(reason, 0) + 1
