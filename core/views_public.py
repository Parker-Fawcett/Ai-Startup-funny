"""Public marketing views: comparison SEO pages, sitemap.xml, robots.txt.

Move 2's distribution asset. These pages are intentionally public — they
exist to rank for buyer-research searches ("Tank Track vs", "ServiceCore
alternative") where the vertical's third-party review base is thin enough
to own. Every competitive number comes from ``marketing_data`` so pages
cannot drift from verified figures, and estimates stay flagged.
"""

from datetime import UTC
from datetime import datetime as utc_datetime

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from core import payments
from core.billing_models import Invoice, InvoiceStatus, PaymentMethod
from core.forms import SignupForm
from core.funnel import track
from core.marketing_data import (
    CANONICAL_PATHS,
    COMPETITORS,
    DISCLAIMER,
    FOUNDING_OFFER,
    PLANS,
    PRICING_AS_OF,
    PUMPRUN,
    competitor,
)
from core.models import Organization


def compare_index(request: HttpRequest) -> HttpResponse:
    """Hub page linking the three head-to-head comparisons."""
    return render(
        request,
        "core/compare/index.html",
        {"competitors": COMPETITORS, "pumprun": PUMPRUN, "disclaimer": DISCLAIMER},
    )


def compare_tank_track(request: HttpRequest) -> HttpResponse:
    """Rank for "Tank Track vs": per-truck math, rate lock, invoicing, compliance."""
    return _render_compare(request, "tank-track")


def compare_servicecore(request: HttpRequest) -> HttpResponse:
    """Rank for "ServiceCore alternative": speed and contract contrast."""
    return _render_compare(request, "servicecore")


def compare_pumpdocket(request: HttpRequest) -> HttpResponse:
    """Rank for "PumpDocket vs": maintained filing logic vs cited links."""
    return _render_compare(request, "pumpdocket")


def robots_txt(request: HttpRequest) -> HttpResponse:
    """Allow crawlers everywhere except the admin; point at the sitemap."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse(("\n".join(lines) + "\n").encode(), content_type="text/plain")


def sitemap_xml(request: HttpRequest) -> HttpResponse:
    """Hand-rolled sitemap of public pages with today's lastmod — nothing auth-gated."""
    lastmod = timezone.localdate().isoformat()
    paths = ["/", *CANONICAL_PATHS]
    entries = "".join(
        f"<url><loc>{request.build_absolute_uri(path)}</loc><lastmod>{lastmod}</lastmod></url>"
        for path in paths
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{entries}</urlset>"
    )
    return HttpResponse(xml.encode(), content_type="application/xml")


def _render_compare(request: HttpRequest, slug: str) -> HttpResponse:
    """Shared renderer: verified facts in context, unique copy per template."""
    return render(
        request,
        f"core/compare/{slug.replace('-', '_')}.html",
        {
            "competitor": competitor(slug),
            "competitors": COMPETITORS,
            "pumprun": PUMPRUN,
            "disclaimer": DISCLAIMER,
            "as_of": PRICING_AS_OF,
        },
    )


def invoice_public(request: HttpRequest, token: str) -> HttpResponse:
    """Customer-facing invoice page reached from the texted or emailed link.

    Deliberately login-free: the token is the only credential, it grants this
    one bill and nothing else, and customers open these on phones in trucks.
    A returning ``?session_id`` is re-verified against Stripe before the bill
    flips to paid — the query string alone is never trusted.
    """
    invoice = get_object_or_404(Invoice, public_token=token)
    session_id = request.GET.get("session_id")
    if session_id:
        try:
            settled = payments.session_paid(session_id)
        except payments.StripeError:
            messages.warning(request, "Could not confirm that payment just now.")
        else:
            if settled:
                invoice.mark_paid(PaymentMethod.CARD_LINK, timezone.localdate())
        return redirect("invoice_public", token=token)

    pay_url = (
        reverse("invoice_pay_stripe", args=[token])
        if payments.enabled() and invoice.status == InvoiceStatus.DUE.value
        else None
    )
    return render(
        request,
        "core/invoice_public.html",
        {"invoice": invoice, "pay_url": pay_url},
    )


def invoice_pay_stripe(request: HttpRequest, token: str) -> HttpResponse:
    """Send the customer to Stripe's hosted Checkout for this exact total."""
    invoice = get_object_or_404(Invoice, public_token=token)
    fallback = redirect("invoice_public", token=token)
    if not payments.enabled() or invoice.status != InvoiceStatus.DUE.value:
        return fallback
    try:
        session = payments.create_checkout_session(
            invoice_number=invoice.number,
            title=f"{invoice.organization.name} — {invoice.number}",
            total=invoice.total,
            customer_email=invoice.job.customer.email,
            token=token,
            base_url=request.build_absolute_uri("/"),
        )
    except payments.StripeError:
        messages.warning(request, "Card payment is temporarily unavailable — call the office.")
        return fallback
    return redirect(session["url"])


def signup(request: HttpRequest) -> HttpResponse:
    """Self-serve trial start: one form creates the shop and logs the owner in.

    The hidden "website" field is a honeypot — humans never see it, so a
    filled value means bot and gets bounced without an error page to scrape.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        if request.POST.get("website"):
            return redirect("pricing")
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.create_user(
                username=email, email=email, password=form.cleaned_data["password1"]
            )
            with transaction.atomic():
                organization = Organization.objects.create(
                    name=form.cleaned_data["shop_name"], owner=user
                )
                auth_login(request, user)
                track("signup_created", organization=organization)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "core/signup.html", {"form": form})


def title5_kit(request: HttpRequest) -> HttpResponse:
    """Lead magnet: the MA Title-5 pumping-form kit, emailed or downloaded."""
    if request.method == "POST":
        form_email = (request.POST.get("email") or "").strip().lower()
        if form_email and "@" in form_email:
            from core.marketing_models import Lead  # noqa: PLC0415 -- avoids app-init cycle

            Lead.objects.update_or_create(email=form_email, defaults={"source": "title5_kit"})
        return redirect("title5_kit_done")
    return render(request, "core/title5_kit.html")


def title5_kit_pdf(request: HttpRequest) -> HttpResponse:  # noqa: ARG001 -- URL resolver passes it
    """Serve the generated Title-5 kit PDF."""
    from core.title5_kit import render_kit_pdf  # noqa: PLC0415 -- keeps reportlab lazy

    response = HttpResponse(render_kit_pdf(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="pumprun-title5-kit.pdf"'
    return response


def title5_kit_done(request: HttpRequest) -> HttpResponse:
    """Post-capture confirmation page."""
    return render(request, "core/title5_kit_done.html")


def home(request: HttpRequest) -> HttpResponse:
    """Public landing page: the crawlable front door."""
    return render(request, "core/home.html")


def pricing(request: HttpRequest) -> HttpResponse:
    """Public plan page; numbers live in marketing_data so copy cannot drift."""
    from core.marketing_models import CaseStudy  # noqa: PLC0415 -- avoids app-init cycle

    track("visited_pricing")
    references = CaseStudy.objects.filter(published=True, is_callable=True)[:3]
    return render(
        request,
        "core/pricing.html",
        {
            "plans": PLANS,
            "plans_contract": PUMPRUN["contract"],
            "founding": FOUNDING_OFFER,
            "callable_references": references,
            "callable_count": CaseStudy.objects.filter(published=True, is_callable=True).count(),
        },
    )


def health(request: HttpRequest) -> HttpResponse:  # noqa: ARG001 -- probe contract takes request
    """Liveness probe for platform health checks; auth-free by design."""
    return JsonResponse({"ok": True})


PLAN_SLUGS = ("solo", "shop", "fleet")


def billing_subscribe(request: HttpRequest, org_pk: int, plan: str) -> HttpResponse:
    """Send the owner to Stripe Checkout to start a 30-day trial subscription."""
    organization = get_object_or_404(Organization, pk=org_pk)
    if plan not in PLAN_SLUGS:
        raise Http404("unknown plan")
    price_id = payments.price_for_plan(plan)
    fallback = redirect("pricing")
    if not price_id or not payments.enabled():
        return fallback
    try:
        session = payments.create_subscription_session(
            organization_id=organization.pk,
            plan=plan,
            price_id=price_id,
            customer_email=request.user.email,
            base_url=request.build_absolute_uri("/"),
        )
    except payments.StripeError:
        messages.warning(request, "Checkout is temporarily unavailable — try again shortly.")
        return fallback
    return redirect(session["url"])


def billing_callback(request: HttpRequest, org_pk: int) -> HttpResponse:
    """Verify the Checkout Session server-side, then persist subscription truth."""
    organization = get_object_or_404(Organization, pk=org_pk)
    session_id = request.GET.get("session_id", "")
    plan = request.GET.get("plan", "")
    try:
        sub = payments.session_subscription(session_id)
    except payments.StripeError:
        messages.warning(request, "Could not confirm the subscription just now.")
        return redirect("dashboard")

    trial_end = sub.get("trial_end")
    organization.plan = plan if plan in PLAN_SLUGS else organization.plan
    organization.stripe_subscription_id = str(sub.get("id") or "")
    organization.subscription_status = str(sub.get("status") or "")
    organization.stripe_customer_id = str(
        (sub.get("customer") or "") if isinstance(sub.get("customer"), str) else ""
    )
    if isinstance(trial_end, int):
        organization.trial_ends_on = utc_datetime.fromtimestamp(trial_end, tz=UTC).date()
    organization.save()
    track("subscription_started", organization=organization, plan=organization.plan)
    messages.success(
        request, f"Subscription active — {organization.plan} plan, 30-day trial started."
    )
    return redirect("dashboard")
