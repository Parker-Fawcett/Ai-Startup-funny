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
        "name": "Solo",
        "price": "$299/mo",
        "trucks": "1-3 trucks",
        "features": "CSV import, nearest-neighbor routes, tap-complete with photos, "
        "auto-invoices + customer pay links, due-soon email reminders, monthly "
        "bookkeeper CSV (QuickBooks import), MA 14-day filing clock + board PDFs, "
        "tank ledger with route-sale export.",
    },
    {
        "name": "Fleet",
        "price": "$499/mo",
        "trucks": "4-10 trucks",
        "features": "Everything in Solo plus driver assignment per route day and bulk "
        "compliance exports across the whole book.",
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
