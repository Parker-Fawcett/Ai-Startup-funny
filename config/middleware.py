"""Tiny security-header middleware for policies Django 6.1 doesn't ship."""

from django.conf import settings


class SecurityHeadersMiddleware:
    """Attach Permissions-Policy and CSP on every response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(settings, "CONTENT_SECURITY_POLICY", ""):
            response.headers["Content-Security-Policy"] = settings.CONTENT_SECURITY_POLICY
        policy = getattr(settings, "PERMISSIONS_POLICY", {})
        if policy:
            response.headers["Permissions-Policy"] = ", ".join(
                f"{feature}=()" for feature, allowlist in policy.items() if not allowlist
            )
        return response
