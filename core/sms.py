"""Twilio SMS bridge over the raw REST API — stdlib only, like payments.py.

Transactional service reminders are the TCPA-safe use case (established
business relationship + opt-out in every message). The channel is inert
without the three TWILIO_* env settings; nothing hardcodes credentials.
"""

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from django.conf import settings

_API = "https://api.twilio.com/2010-04-01"


class SmsError(Exception):
    """Delivery failure; callers count it and keep processing the batch."""


def enabled() -> bool:
    """Report whether SMS delivery is configured for this process."""
    return bool(
        settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_FROM_NUMBER
    )


def send_sms(to: str, body: str) -> dict[str, Any]:
    """Send one message via Twilio's Messages resource."""
    if not enabled():
        raise SmsError("SMS is not configured (missing TWILIO_* settings)")
    endpoint = f"{_API}/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
    payload = urllib.parse.urlencode(
        {"To": to, "From": settings.TWILIO_FROM_NUMBER, "Body": body}
    ).encode()
    request = urllib.request.Request(  # noqa: S310 -- https pinned via _API constant
        endpoint, data=payload, method="POST"
    )
    token = base64.b64encode(f"{settings.TWILIO_ACCOUNT_SID}:{settings.TWILIO_AUTH_TOKEN}".encode())
    request.add_header("Authorization", f"Basic {token.decode()}")
    try:
        with urllib.request.urlopen(  # noqa: S310 -- https pinned via _API constant
            request, timeout=15
        ) as response:
            return dict(json.loads(response.read()))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise SmsError(str(error)) from error
