from datetime import date

from core.scheduling import compute_next_due


class TestComputeNextDue:
    def test_adds_interval_months_when_day_fits(self):
        result = compute_next_due(date(2026, 1, 15), 36)

        assert result == date(2029, 1, 15)

    def test_clamps_month_end_to_shorter_target_month(self):
        result = compute_next_due(date(2026, 1, 31), 1)

        assert result == date(2026, 2, 28)

    def test_clamps_month_end_preserving_leap_day(self):
        result = compute_next_due(date(2024, 1, 31), 1)

        assert result == date(2024, 2, 29)

    def test_crosses_year_boundary(self):
        result = compute_next_due(date(2026, 11, 10), 3)

        assert result == date(2027, 2, 10)
