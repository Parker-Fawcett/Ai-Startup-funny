"""Marketing asset models: verifiable customer references (Move 2).

Distribution is the binding constraint, not features: twelve named, callable
customers outrank the vertical's entire THIRD-PARTY review base (~520 reviews
across G2/Capterra combined; rivals' only ratings are first-party testimonials
on their own sites).
``CaseStudy`` is the reference ledger — one row per logo the founder can put
a prospect on the phone with.

Split out of ``models.py`` to honor the 250-LOC ceiling, mirroring
``compliance_models``.
"""

from django.db import models

from core.models import Organization


class CaseStudy(models.Model):
    """One customer story with outcomes and a call-permission flag.

    ``is_callable`` means the customer agreed to take reference calls — the
    only proof class that beats reviews in a word-of-mouth trade. ``sample``
    marks placeholder content written before real references exist; sample
    rows must never publish as social proof. The organization link is
    provenance only (nullable, SET_NULL): references survive a shop record
    being deleted and seeds never fabricate an organization row.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="case_studies",
    )
    title = models.CharField(max_length=200, help_text="Customer-facing company name")
    location = models.CharField(max_length=120, blank=True)
    trucks = models.PositiveSmallIntegerField(null=True, blank=True)
    quote = models.TextField(help_text="The customer's words, verbatim once verified")
    outcome = models.TextField(help_text="Hours saved, filings on time, route-sale value")
    contact_name = models.CharField(max_length=120, blank=True)
    is_callable = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    sample = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-is_callable", "title")

    def __str__(self) -> str:
        flag = "callable" if self.is_callable else "reference"
        return f"{self.title} ({flag})"


class Lead(models.Model):
    """A not-ready-yet buyer who took the free compliance kit.

    The trade researches once every 3-5 years; capturing the email of a
    future buyer today is cheaper than finding them when they're finally
    ready. Source records which magnet converted.
    """

    email = models.EmailField(unique=True)
    source = models.CharField(max_length=32, default="title5_kit")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.email} ({self.source})"
