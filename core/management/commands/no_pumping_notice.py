"""Generate the monthly no-pumping notice some Boards of Health require.

Towns like Mendon (MA) fine haulers who skip the paperwork even in a month
with zero pump-outs. Nobody automates this artifact; it takes one command and
closes a compliance loop no rival touches.
"""

import argparse
import datetime
import pathlib

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.services import get_default_organization

_LETTER = """Board of Health
{town_line}

RE: Monthly No-Pumping Notice — {month_name} {year}

To the Members of the Board:

This letter certifies that {org} performed NO septic pumping or hauling
activities within your jurisdiction during {month_name} {year}, per the
requirement to file a written notice when no pumping was performed.

Licensee / hauler: ______________________________   License no.: __________

Respectfully,
{signer}
{today}
"""


class Command(BaseCommand):
    """Write a fill-in-the-town monthly certification letter."""

    help = "Render the monthly 'no septic pumping performed' notice letter."

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Year/month target plus optional town and output file."""
        parser.add_argument("year", type=int)
        parser.add_argument("month", type=int)
        parser.add_argument("--town", default="")
        parser.add_argument("--out", default="")

    def handle(self, *args: object, **options: object) -> None:  # noqa: ARG002 -- BaseCommand contract
        """Render, then write to --out or print for piping into a mailer."""
        year: int = options["year"]
        month: int = options["month"]
        town: str = options["town"]  # type: ignore[assignment]
        out: str = options["out"]  # type: ignore[assignment]
        try:
            first = datetime.date(year, month, 1)
        except ValueError as error:
            raise CommandError(f"bad month: {error}") from error
        if out and not town:
            raise CommandError("--town is required when writing --out")

        letter = _LETTER.format(
            town_line=town or "____________________",
            month_name=first.strftime("%B"),
            year=year,
            org=get_default_organization().name,
            signer="____________________",
            today=timezone.localdate().isoformat(),
        )
        if out:
            path = pathlib.Path(out)
            path.write_text(letter)
            self.stdout.write(f"wrote {path}")
        else:
            self.stdout.write(letter)
