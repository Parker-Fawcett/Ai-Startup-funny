"""Stripe Checkout bridge over the raw REST API — zero third-party dependencies.

Card capture completes the same-day money loop: the customer's pay link leads
to Stripe's hosted page, and settlement is confirmed by reading the session
server-side (never by trusting the returning query string). The whole bridge
is inert without ``STRIPE_SECRET_KEY`` so dev and trial installs keep working.
"""

import json
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal
from typing import Any

from django.conf import settings

_API_BASE = "https://api.stripe.com/v1"
_TIMEOUT_SECONDS = 15


class StripeError(Exception):
    """Network/API failure; callers fall back to manual payment instructions."""


def enabled() -> bool:
    """Report whether card capture is configured for this process."""
    return bool(settings.STRIPE_SECRET_KEY)


def _request(method: str, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    data = urllib.parse.urlencode(params).encode() if params else None
    # Scheme is pinned by _API_BASE above; only /checkout/sessions paths are hit.
    request = urllib.request.Request(_API_BASE + path, data=data, method=method)  # noqa: S310
    request.add_header("Authorization", f"Bearer {settings.STRIPE_SECRET_KEY}")
    try:
        with urllib.request.urlopen(  # noqa: S310 -- https pinned via _API_BASE constant
            request, timeout=_TIMEOUT_SECONDS
        ) as response:
            return dict(json.loads(response.read()))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise StripeError(str(error)) from error


def create_checkout_session(  # noqa: PLR0913 -- mirrors Stripe's flat form fields
    *,
    invoice_number: str,
    title: str,
    total: Decimal,
    customer_email: str,
    token: str,
    base_url: str,
) -> dict[str, Any]:
    """Create a hosted Checkout Session for one invoice total."""
    params = {
        "mode": "payment",
        "success_url": f"{base_url}/i/{token}/?session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url": f"{base_url}/i/{token}/",
        "client_reference_id": invoice_number,
        "line_items[0][quantity]": "1",
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][unit_amount]": str(int(total * 100)),
        "line_items[0][price_data][product_data][name]": title,
    }
    if customer_email:
        params["customer_email"] = customer_email
    return _request("POST", "/checkout/sessions", params)


def session_paid(session_id: str) -> bool:
    """Confirm server-side that the Checkout Session actually settled."""
    session = _request("GET", f"/checkout/sessions/{urllib.parse.quote(session_id)}")
    return session.get("payment_status") == "paid"


def amount_cents(total: Decimal) -> int:
    """Stripe wants integer cents; quantize through Decimal to dodge float dust."""
    return int((total * 100).quantize(Decimal(1)))


def create_subscription_session(
    *,
    organization_id: int,
    plan: str,
    price_id: str,
    customer_email: str,
    base_url: str,
) -> dict[str, Any]:
    """Start a subscription Checkout with a 30-day trial, card optional."""
    params = {
        "mode": "subscription",
        "success_url": (
            f"{base_url}/billing/{organization_id}/done/"
            "?session_id={CHECKOUT_SESSION_ID}&plan=" + plan
        ),
        "cancel_url": f"{base_url}/pricing/",
        "client_reference_id": str(organization_id),
        "subscription_data[trial_period_days]": "30",
        "line_items[0][quantity]": "1",
        "line_items[0][price]": price_id,
    }
    if customer_email:
        params["customer_email"] = customer_email
    return _request("POST", "/checkout/sessions", params)


def session_subscription(session_id: str) -> dict[str, Any]:
    """Fetch the Checkout Session then its Subscription for server-side truth."""
    session = _request("GET", f"/checkout/sessions/{urllib.parse.quote(session_id)}")
    subscription_id = session.get("subscription")
    if not subscription_id:
        return {}
    return _request("GET", f"/subscriptions/{urllib.parse.quote(str(subscription_id))}")


def price_for_plan(plan: str) -> str:
    """Resolve the env-configured Stripe Price ID for a plan slug."""
    prices = {
        "solo": settings.STRIPE_PRICE_SOLO,
        "shop": settings.STRIPE_PRICE_SHOP,
        "fleet": settings.STRIPE_PRICE_FLEET,
    }
    return prices.get(plan, "")
