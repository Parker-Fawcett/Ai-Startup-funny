"""Template context helpers."""

from django.http import HttpRequest
from django.utils import timezone


def today(request: HttpRequest) -> dict[str, object]:  # noqa: ARG001 -- framework contract
    """Expose the operator's local date to every template."""
    return {"today": timezone.localdate()}
