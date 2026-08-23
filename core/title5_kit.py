"""Title 5 compliance kit: printable PDF generated on the fly."""

import io

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

_SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "1. What 310 CMR 15.351 requires",
        (
            "Every septic tank must be pumped whenever needed - typically at least every 3 years.",
            "The pumper must note the system's condition on a DEP-approved pumping form.",
            "That form goes to the town's Approving Authority within 14 DAYS of the pump-out.",
            "Towns may add rules: monthly no-pumping notices, licenses, or their own forms.",
        ),
    ),
    (
        "2. The System Pumping Record (Form 4) - fields you must capture",
        (
            "Property location and owner; date pumped; system type (septic/tight tank/cesspool).",
            "Quantity pumped (gallons); effluent tee condition; filter present? cleaned?",
            "Condition of system; pumper name, license, and signature.",
        ),
    ),
    (
        "3. Pre-departure checklist",
        (
            "[ ] Gallons measured and recorded   [ ] Filter serviced (cleaned/replaced)",
            "[ ] Tank condition noted (baffle/tee/risers)   [ ] Photo of lid + yard taken",
            "[ ] Form 4 filled and copied   [ ] Filed with town BOH within 14 days",
        ),
    ),
    (
        "4. How PumpRun automates this",
        (
            "Every completed job captures these exact fields and generates the board-ready",
            "record automatically, with a per-job filing receipt log so nothing slips past",
            "the 14-day clock. Free trial at pumprun-x4ic.onrender.com.",
        ),
    ),
)

_DISCLAIMER = (
    "Operational reference only - not legal advice. Confirm local requirements with your board."
)


def render_kit_pdf() -> bytes:
    """Render the kit as a single-page landscape-free letter PDF."""
    buffer = io.BytesIO()
    pdf = Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setTitle("PumpRun - MA Title 5 Pumping Record Kit")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(inch, height - inch, "MA Title 5 Pumping Record Kit")
    pdf.setFont("Helvetica", 11)
    subtitle = "What the law requires, the form your Board of Health expects, and a checklist."
    pdf.drawString(inch, height - inch - 0.35 * inch, subtitle)

    y = height - 2 * inch
    for heading, lines in _SECTIONS:
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(inch, y, heading)
        y -= 0.28 * inch
        pdf.setFont("Helvetica", 10.5)
        for line in lines:
            pdf.drawString(inch + 0.15 * inch, y, line)
            y -= 0.24 * inch
        y -= 0.2 * inch

    pdf.setFont("Helvetica-Oblique", 8.5)
    pdf.drawCentredString(width / 2, 0.6 * inch, _DISCLAIMER)
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
