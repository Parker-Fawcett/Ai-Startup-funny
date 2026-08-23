"""CSV boundary parsing for customer list imports."""

import csv
import io
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Final, assert_never

_REQUIRED_COLUMNS: Final[tuple[str, ...]] = ("name", "address")
_DEFAULT_INTERVAL_MONTHS: Final[int] = 36


@dataclass(frozen=True, slots=True)
class CustomerRow:
    """A validated customer record parsed out of an uploaded CSV."""

    name: str
    address: str
    city: str = ""
    state: str = ""
    zip_code: str = ""
    email: str = ""
    phone: str = ""
    tank_size_gallons: int | None = None
    pump_interval_months: int = _DEFAULT_INTERVAL_MONTHS
    last_pumped: date | None = None


@dataclass(frozen=True, slots=True)
class RowError:
    """One rejected CSV row, located by its 1-based position including the header."""

    row_number: int
    reason: str


@dataclass(frozen=True, slots=True)
class ImportResult:
    """Everything salvageable from one upload, plus everything rejected."""

    rows: tuple[CustomerRow, ...]
    errors: tuple[RowError, ...]


def parse_customers_csv(text: str) -> ImportResult:
    """Parse uploaded CSV text into validated ``CustomerRow`` records or per-row errors."""
    reader = csv.DictReader(io.StringIO(text))
    fieldnames = reader.fieldnames or []
    missing = [column for column in _REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        reason = f"missing required column(s): {', '.join(missing)}"
        return ImportResult(rows=(), errors=(RowError(row_number=1, reason=reason),))

    rows: list[CustomerRow] = []
    errors: list[RowError] = []
    for row_number, raw_row in enumerate(reader, start=2):
        outcome = _build_row(row_number, raw_row)
        match outcome:
            case CustomerRow():
                rows.append(outcome)
            case RowError():
                errors.append(outcome)
            case unreachable:
                assert_never(unreachable)
    return ImportResult(rows=tuple(rows), errors=tuple(errors))


def _build_row(row_number: int, raw_row: Mapping[str, str | None]) -> CustomerRow | RowError:
    """Convert one CSV mapping into a ``CustomerRow`` or a located rejection."""
    name = _cell(raw_row, "name")
    address = _cell(raw_row, "address")
    if not name:
        return RowError(row_number, "name is required")
    if not address:
        return RowError(row_number, "address is required")

    tank_size_gallons = _optional_int(row_number, raw_row, "tank_size_gallons")
    if isinstance(tank_size_gallons, RowError):
        return tank_size_gallons

    pump_interval_months = _optional_int(row_number, raw_row, "pump_interval_months")
    if isinstance(pump_interval_months, RowError):
        return pump_interval_months

    last_pumped = _optional_iso_date(row_number, raw_row, "last_pumped")
    if isinstance(last_pumped, RowError):
        return last_pumped

    return CustomerRow(
        name=name,
        address=address,
        city=_cell(raw_row, "city"),
        state=_cell(raw_row, "state"),
        zip_code=_cell(raw_row, "zip"),
        email=_cell(raw_row, "email"),
        phone=_cell(raw_row, "phone"),
        tank_size_gallons=tank_size_gallons,
        pump_interval_months=(
            pump_interval_months if pump_interval_months is not None else _DEFAULT_INTERVAL_MONTHS
        ),
        last_pumped=last_pumped,
    )


def _cell(raw_row: Mapping[str, str | None], column: str) -> str:
    return (raw_row.get(column) or "").strip()


def _optional_int(
    row_number: int, raw_row: Mapping[str, str | None], column: str
) -> int | RowError | None:
    raw_value = _cell(raw_row, column)
    if not raw_value:
        return None
    try:
        value = int(raw_value)
    except ValueError:
        return RowError(row_number, f"{column}: '{raw_value}' is not a whole number")
    if value < 0:
        return RowError(row_number, f"{column}: '{raw_value}' must be 0 or greater")
    if column == "pump_interval_months" and value == 0:
        return RowError(row_number, f"{column}: '{raw_value}' must be at least 1")
    return value


def _optional_iso_date(
    row_number: int, raw_row: Mapping[str, str | None], column: str
) -> date | RowError | None:
    raw_value = _cell(raw_row, column)
    if not raw_value:
        return None
    try:
        return datetime.strptime(raw_value, "%Y-%m-%d").date()
    except ValueError:
        return RowError(row_number, f"{column}: expected YYYY-MM-DD, got '{raw_value}'")
