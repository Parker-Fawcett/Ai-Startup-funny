"""Pure scheduling math: statutory pump-cycle due dates."""

import calendar
from datetime import date


def compute_next_due(last_pumped: date, interval_months: int) -> date:
    """Advance ``last_pumped`` by ``interval_months``, clamping to the target month's end."""
    months_from_epoch = last_pumped.month - 1 + interval_months
    year = last_pumped.year + months_from_epoch // 12
    month = months_from_epoch % 12 + 1
    last_day_of_target = calendar.monthrange(year, month)[1]
    return date(year, month, min(last_pumped.day, last_day_of_target))
