"""Admin registration: free back-office CRUD for the solo operator."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from core.billing_models import Invoice, RateCard
from core.compliance_models import FilingReceipt, Jurisdiction
from core.exporting import build_route_sale_zip
from core.marketing_models import CaseStudy
from core.media_models import JobAttachment
from core.models import Customer, Job, Organization, TankEvent
from core.services import get_default_organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Back office for the shop profile."""

    list_display = ("name",)


class TankEventInline(admin.TabularInline):
    """The tank's running balance sheet, read from the customer page."""

    model = TankEvent
    extra = 0
    fields = ("event_date", "gallons", "disposal_site", "source", "job", "notes")
    show_change_link = True


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Route-book CRUD with due-date browsing and one-click diligence exports."""

    list_display = (
        "name",
        "address",
        "parcel_id",
        "email",
        "next_due",
        "last_reminded_on",
        "tank_size_gallons",
        "last_pumped",
    )
    list_filter = ("state",)
    search_fields = ("name", "address", "parcel_id")
    date_hierarchy = "next_due"
    actions = ("export_route_sale_package", "mark_sms_opt_out")
    inlines = (TankEventInline,)

    @admin.action(description="Mark opted out of SMS reminders")
    def mark_sms_opt_out(self, request: HttpRequest, queryset: QuerySet[Customer]) -> None:
        """TCPA hygiene: one click silences texts for the selected accounts."""
        updated = queryset.update(sms_opt_out=True)
        self.message_user(request, f"{updated} customer(s) opted out of SMS.")

    @admin.action(description="Download route-sale package (ZIP)")
    def export_route_sale_package(
        self,
        request: HttpRequest,  # noqa: ARG002 -- admin action contract fixes the signature
        queryset: QuerySet[Customer],
    ) -> HttpResponse:
        """Zip the whole book's ledger and due dates as of today for diligence."""
        as_of = timezone.localdate()
        owner = queryset.first()
        organization = owner.organization if owner is not None else get_default_organization()
        payload = build_route_sale_zip(organization, as_of)
        response = HttpResponse(content_type="application/zip")
        filename = f"route-sale-{as_of.isoformat()}.zip"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.content = payload
        return response


class JobAttachmentInline(admin.TabularInline):
    """Field photos captured at the stop."""

    model = JobAttachment
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Day-by-day job inspection with Form 4 detail and media."""

    list_display = ("route_day", "position", "customer", "status", "gallons", "filter_action")
    list_filter = ("status", "filter_action")
    date_hierarchy = "route_day"
    inlines = (JobAttachmentInline,)


@admin.register(TankEvent)
class TankEventAdmin(admin.ModelAdmin):
    """Ledger inspection across the whole book."""

    list_display = ("event_date", "customer", "gallons", "disposal_site", "source", "job")
    list_filter = ("source",)
    date_hierarchy = "event_date"
    search_fields = ("customer__name", "disposal_site", "notes")


@admin.register(Jurisdiction)
class JurisdictionAdmin(admin.ModelAdmin):
    """The living compliance dataset: one row per rule, per window.

    Superseded rules are closed with ``effective_to`` and a new row opened —
    never edited in place — so historical jobs keep the rule in force when
    they were serviced.
    """

    list_display = (
        "state",
        "town",
        "filing_rule",
        "deadline_days",
        "form_variant",
        "effective_from",
        "effective_to",
    )
    list_filter = ("state",)
    search_fields = ("town", "county", "filing_rule", "form_variant")


@admin.register(FilingReceipt)
class FilingReceiptAdmin(admin.ModelAdmin):
    """Proof-of-filing inspection per job."""

    list_display = ("job", "jurisdiction", "filed_on", "filed_by", "receipt_ref")
    list_filter = ("jurisdiction__state",)
    date_hierarchy = "filed_on"
    search_fields = ("filed_by", "receipt_ref")


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    """The reference bench: earn the logo, capture the outcome, flip callable.

    ``is_callable`` is the whole point — a prospect who can phone a peer
    converts without founder hours. Sample rows stay uncallable until a real
    customer signs off.
    """

    list_display = ("title", "location", "trucks", "is_callable", "published", "sample")
    list_filter = ("is_callable", "published", "sample")
    search_fields = ("title", "quote", "outcome")


@admin.register(RateCard)
class RateCardAdmin(admin.ModelAdmin):
    """Per-shop pricing that drives auto-generated invoices."""

    list_display = ("organization", "base_price", "included_gallons", "trip_fee", "disposal_fee")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Every bill the app has minted, with settlement state at a glance."""

    list_display = (
        "number",
        "job",
        "status",
        "total",
        "issued_on",
        "paid_on",
        "payment_method",
    )
    list_filter = ("status", "payment_method")
    search_fields = ("number", "job__customer__name")
    readonly_fields = ("lines", "public_token")
