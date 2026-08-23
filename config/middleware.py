"""Tiny security-header middleware for policies Django 6.1 doesn't ship."""

from collections.abc import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse


class SecurityHeadersMiddleware:
    """Attach Permissions-Policy and CSP on every response."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Store the next callable in the request/response chain."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Add CSP and a denied-features Permissions-Policy to the response."""
        response = self.get_response(request)
        if getattr(settings, "CONTENT_SECURITY_POLICY", ""):
            response.headers["Content-Security-Policy"] = settings.CONTENT_SECURITY_POLICY
        policy: dict[str, list[str]] = getattr(settings, "PERMISSIONS_POLICY", {})
        if policy:
            denied = ", ".join(f"{feature}=()" for feature, allowlist in policy.items())
            response.headers["Permissions-Policy"] = denied
        return response
