"""Pump-out report PDF rendering."""

import io

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from core.compliance import filing_summary
from core.models import Job

_DISCLAIMER: str = (
    "Operational recordkeeping document. Not legal advice. "
    "Verify local ordinance requirements with your health board."
)


def _jurisdiction_footer(job: Job) -> str:
    """Return the filing line for the receiving board, or '' if unknown."""
    rule = job.customer.resolve_jurisdiction(as_of=job.route_day)
    if rule is None:
        return ""
    return filing_summary(rule.as_rule(), job.route_day)[:110]


def render_job_report_pdf(job: Job) -> bytes:
    """Render one job as a single-page pump-out report suitable for health boards."""
    buffer = io.BytesIO()
    pdf = Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setPageCompression(0)

    pdf.setTitle(f"Pump-Out Report JOB-{job.pk:06d}")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(inch, height - inch, "Septic Pump-Out Report")

    city_line = ""
    if job.customer.city:
        city_line = f", {job.customer.city}, {job.customer.state} {job.customer.zip_code}".rstrip()
    tank = (
        f"{job.customer.tank_size_gallons} gallons"
        if job.customer.tank_size_gallons is not None
        else "not recorded"
    )

    rows: list[tuple[str, str]] = [
        ("Report no.", f"JOB-{job.pk:06d}"),
        ("Service date", f"{job.route_day:%Y-%m-%d}"),
        ("Customer", job.customer.name),
        ("Address", f"{job.customer.address}{city_line}"),
        ("Tank size", tank),
        ("Gallons pumped", str(job.gallons) if job.gallons is not None else "-"),
        ("Filter service", job.get_filter_action_display()),
        ("System type", job.customer.system_type or "-"),
        ("Disposal site", job.disposal_site or "-"),
        ("Technician notes", job.completion_notes or "-"),
    ]

    cursor_y = height - 2 * inch
    for label, value in rows:
        pdf.setFont("Helvetica", 11)
        pdf.drawString(inch, cursor_y, label)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(2.6 * inch, cursor_y, value[:70])
        cursor_y -= 0.42 * inch

    footer_line = _jurisdiction_footer(job)
    if footer_line:
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawCentredString(width / 2, 0.95 * inch, footer_line)

    pdf.setFont("Helvetica-Oblique", 8.5)
    pdf.drawCentredString(width / 2, 0.75 * inch, _DISCLAIMER)

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
