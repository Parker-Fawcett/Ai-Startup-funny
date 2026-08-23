"""Pure job pricing: rate-card math for pump-out invoices.

Money is ``Decimal`` end to end; floats never touch an amount. Rates mirror
how haulers actually quote (validated against live rate cards): a base
pump-out price, per-gallon overage beyond the tank's capacity, plus optional
trip and disposal fees.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

_CENTS = Decimal("0.01")


def _money(amount: Decimal) -> Decimal:
    """Quantize to cents with banker-safe rounding for printed totals."""
    return amount.quantize(_CENTS, rounding=ROUND_HALF_UP)


@dataclass(frozen=True, slots=True)
class LineItem:
    """One printed row on the invoice."""

    label: str
    amount: Decimal


@dataclass(frozen=True, slots=True)
class RateSpec:
    """Shop-configured rates; mirrors the editable ``RateCard`` fields."""

    included_gallons: int = 1000
    base_price: Decimal = Decimal("350.00")
    overage_per_gallon: Decimal = Decimal("0.05")
    trip_fee: Decimal = Decimal("45.00")
    disposal_fee: Decimal = Decimal("50.00")


@dataclass(frozen=True, slots=True)
class PricingResult:
    """Every line that prints, plus the single number the customer pays."""

    lines: tuple[LineItem, ...]
    total: Decimal


def price_job(
    *,
    gallons_pumped: int,
    tank_size_gallons: int | None,
    spec: RateSpec,
) -> PricingResult:
    """Price one completed stop: base + overage beyond capacity + fees."""
    included = tank_size_gallons if tank_size_gallons is not None else spec.included_gallons
    overage_gallons = max(0, gallons_pumped - included)

    lines: list[LineItem] = [LineItem(label="Pump-out service", amount=_money(spec.base_price))]
    if overage_gallons > 0 and spec.overage_per_gallon > 0:
        lines.append(
            LineItem(
                label=f"Overage ({overage_gallons} gal x ${spec.overage_per_gallon}/gal)",
                amount=_money(Decimal(overage_gallons) * spec.overage_per_gallon),
            )
        )
    if spec.trip_fee > 0:
        lines.append(LineItem(label="Trip fee", amount=_money(spec.trip_fee)))
    if spec.disposal_fee > 0:
        lines.append(LineItem(label="Disposal fee", amount=_money(spec.disposal_fee)))

    total = _money(sum((line.amount for line in lines), Decimal(0)))
    return PricingResult(lines=tuple(lines), total=total)
