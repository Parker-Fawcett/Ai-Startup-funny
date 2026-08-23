"""Pure compliance math for New England filing rules.

The filing rules themselves live as data on ``Jurisdiction`` rows (Move 3:
maintained regulatory truth, not copy). Everything in this module is
database-free so the statutory clock and rule resolution are unit-testable in
isolation. MA baseline: 310 CMR 15.351 requires the pumper's DEP-approved
form at the local Approving Authority within 14 days of every pump-out.
"""

import datetime
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

MA_FILING_RULE = "310 CMR 15.351"
MA_DEFAULT_DEADLINE_DAYS = 14


@dataclass(frozen=True)
class FilingRule:
    """One jurisdiction's filing requirement, valid over one date window."""

    state: str
    town: str  # "" = statewide default
    filing_rule: str
    deadline_days: int
    form_variant: str
    effective_from: date
    effective_to: date | None = None

    def in_force_on(self, as_of: date) -> bool:
        """Return True when ``as_of`` falls inside this rule's effective window."""
        started = self.effective_from <= as_of
        not_ended = self.effective_to is None or as_of <= self.effective_to
        return started and not_ended

    @property
    def scope(self) -> str:
        """Human label for where the rule applies."""
        return f"{self.state} · {self.town}" if self.town else f"{self.state} statewide"


def compute_filing_deadline(service_date: date, deadline_days: int) -> date:
    """Advance the statutory clock: N calendar days after the pump-out."""
    return service_date + datetime.timedelta(days=deadline_days)


def days_remaining(deadline: date, today: date) -> int:
    """Days left on the filing clock; negative means the window already closed."""
    return (deadline - today).days


def resolve_jurisdiction(
    *, state: str, town: str, rules: Sequence[FilingRule], as_of: date
) -> FilingRule | None:
    """Pick the most-specific rule in force on ``as_of``.

    Exact-town rules beat their state's default; among same-scope candidates
    the newest ``effective_from`` wins. Matching is case-insensitive because
    towns are typed by hand on customer records.
    """
    wanted_state = state.strip().lower()
    wanted_town = town.strip().lower()
    candidates = [
        rule
        for rule in rules
        if rule.state.strip().lower() == wanted_state and rule.in_force_on(as_of)
    ]
    for scope_town in (wanted_town, ""):
        scoped = [rule for rule in candidates if rule.town.strip().lower() == scope_town]
        if scoped:
            return max(scoped, key=lambda rule: rule.effective_from)
    return None


def filing_summary(rule: FilingRule, service_date: date) -> str:
    """One-line human summary shared by the report footer and dashboard badge."""
    due = compute_filing_deadline(service_date, rule.deadline_days)
    return (
        f"{rule.filing_rule}: file {rule.form_variant} with {rule.scope} "
        f"by {due.isoformat()} ({rule.deadline_days}-day window)"
    )
