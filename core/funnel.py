"""Conversion-funnel instrumentation at founder scale.

Four events tell us whether the self-serve loop works end-to-end:
visited_pricing -> signup_created -> import_completed(rows=n) ->
subscription_started. Internal storage keeps measurement alive without any
third-party account; export later if volume ever justifies it.
"""

from typing import Final

from django.core.exceptions import ValidationError

from core.models import FunnelEvent, Organization

EVENT_NAMES: Final[frozenset[str]] = frozenset(
    {
        "visited_pricing",
        "signup_created",
        "import_completed",
        "subscription_started",
    }
)


def track(name: str, *, organization: Organization | None = None, **meta: object) -> None:
    """Record one funnel event; unknown names fail loudly in tests."""
    if name not in EVENT_NAMES:
        raise ValidationError(f"Unknown funnel event: {name!r}")
    FunnelEvent.objects.create(name=name, organization=organization, meta=dict(meta))
