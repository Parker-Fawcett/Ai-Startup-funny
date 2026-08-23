"""Route-sale diligence packages: zipped CSV snapshots of the tank book.

A route sale is a real event in this trade, and the buyer's first question is
"show me the tanks." This module assembles the point-in-time balance sheet —
every pump-out on record plus the due-date book — so the ledger itself is the
asset being handed over.
"""

import csv
import datetime
import io
import zipfile

from core.models import Organization, TankEvent
from core.scheduling import compute_next_due

_LEDGER_HEADER: tuple[str, ...] = (
    "customer",
    "address",
    "city",
    "state",
    "zip",
    "parcel_id",
    "event_date",
    "gallons",
    "disposal_site",
    "source",
    "job_id",
    "notes",
)

_DUE_HEADER: tuple[str, ...] = (
    "customer",
    "address",
    "parcel_id",
    "tank_size_gallons",
    "last_pumped",
    "pump_interval_months",
    "next_due",
)


def build_route_sale_zip(organization: Organization, as_of: datetime.date) -> bytes:
    """Zip the tank-ledger and due-date CSVs covering everything through ``as_of``."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("tank_ledger.csv", _ledger_csv(organization, as_of))
        bundle.writestr("due_dates.csv", _due_dates_csv(organization, as_of))
    return buffer.getvalue()


def _ledger_csv(organization: Organization, as_of: datetime.date) -> str:
    """Render every ledger event on or before ``as_of``, oldest first per tank."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(_LEDGER_HEADER)
    events = (
        TankEvent.objects.filter(customer__organization=organization, event_date__lte=as_of)
        .select_related("customer")
        .order_by("customer__name", "event_date", "pk")
    )
    for event in events:
        customer = event.customer
        writer.writerow(
            [
                customer.name,
                customer.address,
                customer.city,
                customer.state,
                customer.zip_code,
                customer.parcel_id,
                event.event_date.isoformat(),
                "" if event.gallons is None else event.gallons,
                event.disposal_site,
                event.source,
                "" if event.job_id is None else event.job_id,
                event.notes,
            ]
        )
    return out.getvalue()


def _due_dates_csv(organization: Organization, as_of: datetime.date) -> str:
    """Render the due-date book as it stood at ``as_of`` from recorded pump-outs."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(_DUE_HEADER)
    tracked = organization.customers.filter(last_pumped__lte=as_of).order_by("name")
    for customer in tracked:
        last_pumped = customer.last_pumped
        if last_pumped is None:  # unreachable through the queryset filter; keeps typing honest
            continue
        writer.writerow(
            [
                customer.name,
                customer.address,
                customer.parcel_id,
                "" if customer.tank_size_gallons is None else customer.tank_size_gallons,
                last_pumped.isoformat(),
                customer.pump_interval_months,
                compute_next_due(last_pumped, customer.pump_interval_months).isoformat(),
            ]
        )
    return out.getvalue()


_INVOICE_HEADER: tuple[str, ...] = (
    "invoice_number",
    "issued_on",
    "customer",
    "job_id",
    "route_day",
    "status",
    "total",
    "paid_on",
    "payment_method",
)


def build_invoices_csv(org: Organization, year: int, month: int) -> str:
    """Render one month's invoices as bookkeeper-ready CSV (QuickBooks import).

    One-way export is the market-proven floor: the bookkeeper imports the file
    into QuickBooks and never re-keys a job.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(_INVOICE_HEADER)
    invoices = org.invoices.filter(issued_on__year=year, issued_on__month=month).select_related(
        "job", "job__customer"
    )
    for invoice in invoices:
        writer.writerow(
            (
                invoice.number,
                invoice.issued_on.isoformat(),
                invoice.job.customer.name,
                invoice.job_id,
                invoice.job.route_day.isoformat(),
                invoice.status,
                f"{invoice.total:.2f}",
                invoice.paid_on.isoformat() if invoice.paid_on else "",
                invoice.payment_method or "",
            )
        )
    return buffer.getvalue()
