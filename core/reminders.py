"""Pure reminder logic: who gets a pump-due nudge and what the email says.

The due-date CRM only makes money if it *acts*: whoever reminds the customer
on schedule wins the next pump-out (the 3-5 year cycle is won at reminder
time, not search time). Decision math lives here so it stays unit-testable;
delivery and stamping live in the ``send_reminders`` command.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Final

DEFAULT_WINDOW_DAYS: Final[int] = 30
DEFAULT_MIN_RESEND_DAYS: Final[int] = 60


@dataclass(frozen=True, slots=True)
class ReminderDecision:
    """Outcome for one customer, with the reason for auditability."""

    should_send: bool
    reason: str


def decide(
    *,
    next_due: date | None,
    today: date,
    last_reminded_on: date | None = None,
    window_days: int = DEFAULT_WINDOW_DAYS,
    min_resend_days: int = DEFAULT_MIN_RESEND_DAYS,
) -> ReminderDecision:
    """Decide whether one customer gets a reminder email today.

    Sends when the account is overdue or lands inside the forward window and
    has not been reminded recently; everything else is skipped with a reason.
    """
    if next_due is None:
        return ReminderDecision(should_send=False, reason="no_due_date")
    if next_due > today + timedelta(days=window_days):
        return ReminderDecision(should_send=False, reason="outside_window")
    if last_reminded_on is not None and (today - last_reminded_on).days < min_resend_days:
        return ReminderDecision(should_send=False, reason="recently_reminded")
    urgency = "overdue" if next_due < today else "due_soon"
    return ReminderDecision(should_send=True, reason=urgency)


def render_reminder(
    *, customer_name: str, org_name: str, next_due: date, today: date
) -> tuple[str, str]:
    """Return ``(subject, body)`` for one plain-text reminder email."""
    overdue = next_due < today
    subject = (
        f"{org_name}: your septic pumping is overdue"
        if overdue
        else f"{org_name}: septic pumping due {next_due.isoformat()}"
    )
    body = (
        f"Hi {customer_name},\n\n"
        + (
            f"Your septic system was due for pumping on {next_due.isoformat()} "
            "and hasn't been serviced yet.\n\n"
            if overdue
            else f"A quick heads-up that your septic tank is due for pumping "
            f"on {next_due.isoformat()}.\n\n"
        )
        + f"Reply to this email or call {org_name} to book a stop on an "
        "upcoming route. Regular pumping protects your drain field and keeps "
        "you compliant with local Board of Health requirements.\n\n"
        f"— {org_name}"
    )
    _ = today
    return subject, body


def render_sms(*, org_name: str, next_due: date, today: date) -> str:
    """Return one TCPA-safe transactional reminder text, opt-out included."""
    when = "overdue for pumping" if next_due < today else f"due {next_due.isoformat()}"
    return f"{org_name}: your septic tank is {when}. Call to book. Reply STOP to opt out."
