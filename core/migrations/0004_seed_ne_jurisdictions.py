"""Seed the New England compliance dataset (Move 3 baseline).

Five point-in-time rules: the MA statewide 310 CMR 15.351 14-day filing
default, two MA towns that layer stricter rules on top, and NH/ME statewide
samples. Town rules are never edited in place — close them with
``effective_to`` and open a new row, appending to ``change_log``.
"""

import datetime

from django.db import migrations

SEED_JURISDICTIONS = (
    {
        "state": "MA",
        "town": "",
        "county": "",
        "filing_rule": "310 CMR 15.351",
        "deadline_days": 14,
        "form_variant": "DEP Title 5 Pump-Out Form",
        "effective_from": datetime.date(2016, 1, 1),
        "effective_to": None,
        "change_log": (
            "2016-01-01: Baseline. Pumper must file the DEP-approved pumping "
            "form with the local Approving Authority (Board of Health) within "
            "14 days of every pump-out; system inspection typically valid 3 "
            "years with documented pumping."
        ),
    },
    {
        "state": "MA",
        "town": "Leominster",
        "county": "Worcester",
        "filing_rule": "Leominster BOH Title 5 bylaw",
        "deadline_days": 7,
        "form_variant": "Leominster BOH Pump-Out Certificate",
        "effective_from": datetime.date(2023, 7, 1),
        "effective_to": None,
        "change_log": (
            "2023-07-01: Tightened from 10 to 7 days; inspection validity tied "
            "to documented annual pumping. Verify current wording with BOH."
        ),
    },
    {
        "state": "MA",
        "town": "Westford",
        "county": "Middlesex",
        "filing_rule": "Westford Health Dept. septic reg",
        "deadline_days": 10,
        "form_variant": "Westford Health Dept. Pump-Out Form",
        "effective_from": datetime.date(2024, 1, 1),
        "effective_to": None,
        "change_log": (
            "2024-01-01: Sample town override — 10-day filing window and town "
            "form variant. Verify current wording with Health Dept."
        ),
    },
    {
        "state": "NH",
        "town": "",
        "county": "",
        "filing_rule": "Env-Wq 1000 (Subsurface Systems)",
        "deadline_days": 30,
        "form_variant": "NH DES Pump-Out Report",
        "effective_from": datetime.date(2020, 1, 1),
        "effective_to": None,
        "change_log": (
            "2020-01-01: Sample statewide seed for NE coverage. NH has no "
            "statutory pump-out filing clock comparable to MA; 30 days is an "
            "operational service-level target, not statute. Verify with NH DES."
        ),
    },
    {
        "state": "ME",
        "town": "",
        "county": "",
        "filing_rule": "Subsurface Wastewater Disposal Rules, 144A CMR 241",
        "deadline_days": 30,
        "form_variant": "ME Subsurface Disposal Pump-Out Record",
        "effective_from": datetime.date(2020, 1, 1),
        "effective_to": None,
        "change_log": (
            "2020-01-01: Sample statewide seed for NE coverage. 30 days is an "
            "operational service-level target, not statute. Verify with ME DHS."
        ),
    },
)


def seed_ne_jurisdictions(apps, schema_editor):
    """Insert the baseline dataset once; idempotent per unique scope+start."""
    jurisdiction = apps.get_model("core", "jurisdiction")
    for row in SEED_JURISDICTIONS:
        jurisdiction.objects.update_or_create(
            state=row["state"],
            town=row["town"],
            effective_from=row["effective_from"],
            defaults=row,
        )


def remove_seeded_jurisdictions(apps, schema_editor):
    jurisdiction = apps.get_model("core", "jurisdiction")
    jurisdiction.objects.filter(state__in=("MA", "NH", "ME")).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_jurisdiction_filingreceipt"),
    ]

    operations = [
        migrations.RunPython(seed_ne_jurisdictions, remove_seeded_jurisdictions),
    ]
