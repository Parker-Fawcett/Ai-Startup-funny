"""Public marketing views: comparison SEO pages, sitemap.xml, robots.txt.

Move 2's distribution asset. These pages are intentionally public — they
exist to rank for buyer-research searches ("Tank Track vs", "ServiceCore
alternative") where the vertical's third-party review base is thin enough
to own. Every competitive number comes from ``marketing_data`` so pages
cannot drift from verified figures, and estimates stay flagged.
"""

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from core import payments
from core.billing_models import Invoice, InvoiceStatus, PaymentMethod
from core.forms import SignupForm
from core.marketing_data import (
    CANONICAL_PATHS,
    COMPETITORS,
    DISCLAIMER,
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
    """Hand-rolled sitemap of the public comparison pages — nothing auth-gated."""
    entries = "".join(
        f"<url><loc>{request.build_absolute_uri(path)}</loc></url>" for path in CANONICAL_PATHS
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
            Organization.objects.create(name=form.cleaned_data["shop_name"])
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "core/signup.html", {"form": form})


def pricing(request: HttpRequest) -> HttpResponse:
    """Public plan page; numbers live in marketing_data so copy cannot drift."""
    return render(
        request,
        "core/pricing.html",
        {"plans": PLANS, "plans_contract": PUMPRUN["contract"]},
    )


from django.http import JsonResponse


def health(request: HttpRequest) -> HttpResponse:
    """Liveness probe for platform health checks; auth-free by design."""
    return JsonResponse({"ok": True})
