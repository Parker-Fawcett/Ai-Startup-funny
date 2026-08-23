"""Seed the reference bench with three clearly-marked sample stories (Move 2).

These demonstrate the outcome format the founder should capture (hours saved,
filings on time, route-sale value) but are NOT verified customers: every row
ships ``sample=True`` and ``is_callable=False``. A reference you can't back is
a liability in a word-of-mouth trade — flip ``is_callable`` only after a real
customer agrees to take reference calls.
"""

from django.db import migrations

SEED_CASES = (
    {
        "title": "Pioneer Valley Septic",
        "location": "Springfield, MA",
        "trucks": 3,
        "quote": "The filing clock used to live in my head. Now every tank just has its due date.",
        "outcome": (
            "SAMPLE STORY - replace with verified results before publishing. Shape to "
            "capture: office hours saved per week; every Title 5 pump-out form filed inside "
            "the 14-day Board of Health window since switching."
        ),
        "contact_name": "",
        "is_callable": False,
        "sample": True,
    },
    {
        "title": "Chicopee Valley Septic",
        "location": "Chicopee, MA",
        "trucks": 4,
        "quote": "We added a fourth truck and the software bill didn't move an inch.",
        "outcome": (
            "SAMPLE STORY - replace with verified results before publishing. Shape to "
            "capture: flat price held while per-truck quotes ran higher; route-sale package "
            "exported when buying out a retiring hauler's book."
        ),
        "contact_name": "",
        "is_callable": False,
        "sample": True,
    },
    {
        "title": "Granite State Pumping",
        "location": "Nashua, NH",
        "trucks": 5,
        "quote": "Dead zones on 101 used to mean paperwork at the shop all night.",
        "outcome": (
            "SAMPLE STORY - replace with verified results before publishing. Shape to "
            "capture: offline tap-complete through no-signal stretches; pump-out reports "
            "delivered same-day."
        ),
        "contact_name": "",
        "is_callable": False,
        "sample": True,
    },
)


def seed_case_studies(apps, schema_editor):
    """Insert the bench once, attached to the first organization if one exists.

    Never creates an organization: fresh databases (including test databases)
    get provenance-less samples rather than a phantom tenant that would hijack
    ``get_default_organization()``.
    """
    case_study = apps.get_model("core", "CaseStudy")
    organization = apps.get_model("core", "Organization")
    org = organization.objects.order_by("pk").first()
    for row in SEED_CASES:
        case_study.objects.update_or_create(
            title=row["title"], defaults={**row, "organization": org}
        )


def remove_seeded_cases(apps, schema_editor):
    case_study = apps.get_model("core", "CaseStudy")
    case_study.objects.filter(title__in=[row["title"] for row in SEED_CASES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_casestudy"),
    ]

    operations = [
        migrations.RunPython(seed_case_studies, remove_seeded_cases),
    ]
