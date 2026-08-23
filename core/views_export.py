"""Diligence and bookkeeping exports: the shop's data, always leaveable."""

import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse

from core.exporting import build_invoices_csv, build_route_sale_zip
from core.services import get_default_organization


@login_required
def route_sale_export(request: HttpRequest, route_day: str) -> HttpResponse:  # noqa: ARG001 -- URL resolver passes request
    """Download the whole book's diligence package as of one date.

    The zip carries the tank ledger and the due-date book, point-in-time at
    ``route_day`` — exactly what a buyer (or a departing shop's successor)
    needs to price the routes.
    """
    try:
        day = datetime.date.fromisoformat(route_day)
    except ValueError as error:
        raise Http404(f"bad export date {route_day!r}") from error

    payload = build_route_sale_zip(get_default_organization(), day)
    response = HttpResponse(content_type="application/zip")
    filename = f"route-sale-{day.isoformat()}.zip"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.content = payload
    return response


@login_required
def invoice_export(
    request: HttpRequest,  # noqa: ARG001 -- login decorator consumes request
    year: int,
    month: int,
) -> HttpResponse:
    """Serve one month's invoices as CSV for the bookkeeper's QuickBooks import."""
    try:
        datetime.date(year, month, 1)
    except ValueError as error:
        raise Http404("bad month") from error
    csv_text = build_invoices_csv(get_default_organization(), year, month)
    response = HttpResponse(csv_text, content_type="text/csv")
    filename = f"invoices-{year}-{month:02d}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
