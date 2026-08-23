"""Server-rendered views for the owner app."""

import datetime
from typing import TypedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from core.compliance import compute_filing_deadline, days_remaining
from core.compliance_models import FilingReceipt
from core.forms import CompleteForm, ImportForm
from core.funnel import track
from core.importing import ImportResult, parse_customers_csv
from core.marketing_models import CaseStudy
from core.media_models import JobAttachment
from core.models import Customer, Invoice, Job, JobStatus, Organization, PaymentMethod
from core.reports import render_job_report_pdf
from core.services import build_route, get_default_organization

_STALE_AFTER_DAYS = 30  # filing windows blown by more than this leave the queue


class FilingQueueItem(TypedDict):
    """One dashboard row: a completed stop whose filing window is still relevant."""

    job: Job
    rule_label: str
    form_variant: str
    due: datetime.date
    days_left: int


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Bucket the route book by statutory urgency and show today's plan."""
    organization = get_default_organization()
    today = timezone.localdate()
    tracked = organization.customers.filter(next_due__isnull=False)
    overdue = tracked.filter(next_due__lt=today)
    due_30 = tracked.filter(next_due__gte=today, next_due__lte=today + datetime.timedelta(days=30))
    due_90 = tracked.filter(
        next_due__gt=today + datetime.timedelta(days=30),
        next_due__lte=today + datetime.timedelta(days=90),
    )
    todays_jobs = Job.objects.filter(organization=organization, route_day=today).select_related(
        "customer"
    )
    references = CaseStudy.objects.filter(published=True, is_callable=True)
    prev = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    return render(
        request,
        "core/dashboard.html",
        {
            "overdue": overdue,
            "due_30": due_30,
            "due_90": due_90,
            "todays_jobs": todays_jobs,
            "filings_due": _filing_queue(organization, today),
            "callable_references": references[:5],
            "callable_count": references.count(),
            "today": today,
            "prev_year": prev.year,
            "prev_month": prev.month,
            "prev_month_name": prev.strftime("%B"),
        },
    )


def _filing_queue(
    organization: Organization, today: datetime.date, limit: int = 20
) -> list[FilingQueueItem]:
    """Completed stops whose Board-of-Health filing window is open or recently closed.

    Each entry carries the jurisdiction label, the expected form variant, the
    statutory due date, and days remaining (negative = window blown). Stops
    already covered by a FilingReceipt drop off; anything older than 30 days
    past due is left to history.
    """
    completed = (
        Job.objects.filter(organization=organization, status=JobStatus.COMPLETED)
        .select_related("customer")
        .order_by("-route_day")[:200]
    )
    filed_job_ids = set(FilingReceipt.objects.values_list("job_id", flat=True))
    queue: list[FilingQueueItem] = []
    for job in completed:
        if job.pk in filed_job_ids:
            continue
        rule = job.customer.resolve_jurisdiction(as_of=job.route_day)
        if rule is None:
            continue
        due = compute_filing_deadline(job.route_day, rule.deadline_days)
        days_left = days_remaining(due, today)
        if days_left < -_STALE_AFTER_DAYS:
            continue
        queue.append(
            {
                "job": job,
                "rule_label": str(rule),
                "form_variant": rule.form_variant,
                "due": due,
                "days_left": days_left,
            }
        )
        if len(queue) >= limit:
            break
    return sorted(queue, key=lambda item: item["days_left"])


@login_required
def import_customers(request: HttpRequest) -> HttpResponse:
    """Upload a customer-list CSV; valid rows are created, bad rows are reported."""
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            result = _run_import(
                organization=get_default_organization(),
                text=form.cleaned_data["csv_file"],
            )
            track("import_completed", rows=len(result.rows))
            if not result.errors:
                count = len(result.rows)
                noun = "customer" if count == 1 else "customers"
                messages.success(request, f"Imported {count} {noun}.")
                return redirect("dashboard")
            return render(
                request,
                "core/import.html",
                {"form": form, "errors": result.errors, "imported_count": len(result.rows)},
            )
    else:
        form = ImportForm()
    return render(request, "core/import.html", {"form": form, "errors": None})


def _run_import(organization: Organization, text: str) -> ImportResult:
    result = parse_customers_csv(text)
    Customer.objects.bulk_create(
        [Customer.from_import_row(organization=organization, row=row) for row in result.rows],
        batch_size=500,
    )
    return result


@login_required
def route_day(request: HttpRequest, route_day: str) -> HttpResponse:
    """Pick which accounts run on a day; POST rebuilds the nearest-neighbor plan."""
    try:
        day = datetime.date.fromisoformat(route_day)
    except ValueError as error:
        raise Http404(f"bad route date {route_day!r}") from error

    organization = get_default_organization()
    if request.method == "POST":
        selected_ids = [int(pk) for pk in request.POST.getlist("customers")]
        build_route(organization, day, selected_ids, driver=request.POST.get("driver", "")[:80])
        return redirect("route_day", route_day=day.isoformat())

    today = timezone.localdate()
    pickable = (
        organization.customers.filter(next_due__isnull=True)
        | organization.customers.filter(next_due__lte=today + datetime.timedelta(days=14))
        | organization.customers.filter(next_due__isnull=False, next_due__lt=today)
    )  # type: ignore[attr-defined]
    jobs = Job.objects.filter(organization=organization, route_day=day).select_related("customer")
    return render(
        request,
        "core/route_day.html",
        {"day": day, "pickable": pickable.distinct(), "jobs": jobs},
    )


@login_required
def job_complete(request: HttpRequest, pk: int) -> HttpResponse:
    """Mobile flow: capture report fields, photo, and close out one stop.

    Offline replays can re-POST a closed stop; the guard below makes that a
    friendly no-op so the ledger and invoice never double-book.
    """
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        if job.status == JobStatus.COMPLETED:
            messages.info(
                request, f"{job.customer.name}'s stop was already closed — nothing double-booked."
            )
            return redirect("route_day", route_day=job.route_day.strftime("%Y-%m-%d"))
        form = CompleteForm(request.POST, request.FILES)
        if form.is_valid():
            job.mark_completed(
                gallons=form.cleaned_data["gallons"],
                disposal_site=form.cleaned_data["disposal_site"],
                completion_notes=form.cleaned_data["notes"],
                pumped_on=timezone.localdate(),
                filter_action=form.cleaned_data.get("filter_action") or "none",
                system_type=form.cleaned_data["system_type"],
            )
            photo = form.cleaned_data.get("photo")
            if photo is not None:
                JobAttachment.objects.create(job=job, file=photo)
            return redirect("route_day", route_day=job.route_day.strftime("%Y-%m-%d"))
    else:
        form = CompleteForm(initial={"system_type": job.customer.system_type})
    return render(request, "core/complete.html", {"job": job, "form": form})


@login_required
def job_report_pdf(request: HttpRequest, pk: int) -> HttpResponse:  # noqa: ARG001 -- URL resolver passes request
    """Serve the auto-filled pump-out report for a completed stop."""
    job = get_object_or_404(Job, pk=pk)
    response = HttpResponse(content_type="application/pdf")
    filename = f"pump-out-JOB-{job.pk:06d}.pdf"
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    response.content = render_job_report_pdf(job)
    return response


@login_required
def invoice_mark_paid(request: HttpRequest, pk: int) -> HttpResponse:
    """Record how an issued invoice settled: card link, check, cash, or ACH."""
    if request.method != "POST":
        raise Http404("POST only")
    invoice = get_object_or_404(Invoice, pk=pk)
    method = request.POST.get("payment_method", "")
    if method not in PaymentMethod.values:
        messages.warning(
            request, f"Unknown payment method {method!r}; invoice left {invoice.status}."
        )
    else:
        invoice.mark_paid(method, timezone.localdate())
        messages.success(request, f"{invoice.number} marked paid.")
    return redirect("route_day", route_day=invoice.job.route_day.isoformat())
