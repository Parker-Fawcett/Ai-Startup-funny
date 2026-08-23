"""Verified competitive facts behind the comparison pages (Move 2).

Single source of truth for pricing claims so pages, tests, and the compare
index cannot drift apart. Every figure carries its verification status:
either the vendor's own pricing page (live-read August 2026) or an explicit
"third-party reported" flag. Nothing here is invented; when a vendor moves,
re-verify and update this file first.
"""

PRICING_AS_OF = "August 2026"

DISCLAIMER = (
    f"Pricing was read from vendor pricing pages in {PRICING_AS_OF} and each figure cites "
    "its source. Vendors change prices without notice — confirm current terms before "
    "deciding. Figures labeled 'third-party reported' come from review sites and trackers, "
    "not the vendor. These pages compare products; nothing here is legal advice."
)

PUMPRUN = {
    "name": "PumpRun",
    "price_line": "$299/mo solo · $499/mo fleet — flat, unlimited users",
    "contract": "Month-to-month, cancel anytime, no setup fee. Prepay annual, get 2 months free.",
}

PLANS: tuple[dict[str, str], ...] = (
    {
        "name": "Fleet",
        "price": "$499/mo",
        "trucks": "4-10 trucks",
        "features": "Everything in Shop plus driver assignment per route day and bulk "
        "compliance exports across the whole book.",
    },
    {
        "name": "Shop",
        "price": "$399/mo",
        "trucks": "2-5 trucks",
        "features": "Everything in Solo plus recurring SMS reminders, QuickBooks-ready "
        "bookkeeper CSV, and the tank-ledger route-sale package.",
    },
    {
        "name": "Solo",
        "price": "$299/mo",
        "trucks": "1-3 trucks",
        "features": "CSV import, nearest-neighbor routes, tap-complete with photos, "
        "auto-invoices with customer pay links, due-soon email reminders, "
        "MA 14-day filing clock and board PDFs.",
    },
)

COMPETITORS: tuple[dict[str, str], ...] = (
    {
        "slug": "tank-track",
        "name": "Tank Track",
        "price_line": "$180/mo first truck + $150/mo each additional truck",
        "contract": "Month-to-month; no free trial (60-day money-back guarantee)",
        "source_domain": "tank-track.com",
        "price_note": (
            "Live-verified on tank-track.com pricing, August 2026. Third-party reported: "
            "the same page still showed $149/$125 in late July per an independent tracker — "
            "a roughly 20% increase within weeks of this writing."
        ),
    },
    {
        "slug": "servicecore",
        "name": "ServiceCore",
        "price_line": "Quote-only — pricing is revealed on a demo call",
        "contract": "Annual contract required, billed monthly; 6-12 week onboarding",
        "source_domain": "servicecore.com",
        "price_note": (
            "Live-verified on servicecore.com pricing, August 2026: no dollar figures are "
            "published anywhere on the page. Third-party reported estimates run $200-400+ "
            "per truck per month; treat them as guesses until you have a written quote."
        ),
    },
    {
        "slug": "pumpdocket",
        "name": "PumpDocket",
        "price_line": "$99/mo Starter intro ($139 standard), capped at 75 active customers",
        "contract": "Month-to-month; first month free; no setup fee",
        "source_domain": "pumpdocket.com",
        "price_note": (
            "Live-verified on pumpdocket.com pricing, August 2026. Intro rates are "
            "advertised as locked for life; the standard rates apply if that promo ends. "
            "Third-party reported: zero independent reviews exist yet."
        ),
    },
)

CANONICAL_PATHS: tuple[str, ...] = (
    "/pricing/",
    "/compare/",
    "/compare/tank-track/",
    "/compare/servicecore/",
    "/compare/pumpdocket/",
)


def competitor(slug: str) -> dict[str, str]:
    """Return one competitor's fact sheet by slug."""
    return next(entry for entry in COMPETITORS if entry["slug"] == slug)


FOUNDING_OFFER = {
    "headline": "Founding 10 shops: $199/mo, rate-locked forever",
    "body": "First ten shops get every feature in Fleet at $199/mo — locked for as long as you stay. "
    "In exchange: a candid testimonial after 60 days and permission to reference you.",
    "remaining": 10,
}
