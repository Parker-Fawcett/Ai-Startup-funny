from core.importing import parse_customers_csv

HAPPY_CSV = (
    "name,address,city,state,zip,tank_size_gallons,pump_interval_months,last_pumped\n"
    "Doe Residence,1 Main St,Springfield,MA,01101,1000,36,2026-01-15\n"
    "Corner Diner,9 Elm St,Springfield,MA,01102,,,\n"
)


class TestParseCustomersCsv:
    def test_parses_full_row_into_typed_fields(self):
        result = parse_customers_csv(HAPPY_CSV)

        assert len(result.rows) == 2
        first = result.rows[0]
        assert first.name == "Doe Residence"
        assert first.address == "1 Main St"
        assert first.city == "Springfield"
        assert first.state == "MA"
        assert first.zip_code == "01101"
        assert first.tank_size_gallons == 1000
        assert first.pump_interval_months == 36
        assert str(first.last_pumped) == "2026-01-15"

    def test_optional_fields_default_when_blank(self):
        result = parse_customers_csv(HAPPY_CSV)

        second = result.rows[1]
        assert second.tank_size_gallons is None
        assert second.last_pumped is None
        assert second.pump_interval_months == 36

    def test_missing_required_header_reports_column(self):
        result = parse_customers_csv("name,city\nFoo,Springfield\n")

        assert result.rows == ()
        assert any("address" in error.reason for error in result.errors)

    def test_row_missing_name_is_an_error_with_row_number(self):
        csv_text = "name,address\n,1 Main St\n"

        result = parse_customers_csv(csv_text)

        assert result.rows == ()
        assert result.errors[0].row_number == 2

    def test_bad_integer_reports_error_not_crash(self):
        csv_text = "name,address,tank_size_gallons\nX,1 St,abc\n"

        result = parse_customers_csv(csv_text)

        assert result.rows == ()
        assert any("tank" in error.reason.lower() for error in result.errors)

    def test_bad_date_reports_error_not_crash(self):
        csv_text = "name,address,last_pumped\nX,1 St,not-a-date\n"

        result = parse_customers_csv(csv_text)

        assert result.rows == ()
        assert any("last_pumped" in error.reason for error in result.errors)

    def test_header_only_yields_nothing(self):
        result = parse_customers_csv("name,address\n")

        assert result.rows == ()
        assert result.errors == ()

    def test_crlf_and_surrounding_whitespace_are_normalized(self):
        csv_text = "name,address\r\n  Spaced Shop , 7 Rd  \r\n"

        result = parse_customers_csv(csv_text)

        assert result.rows[0].name == "Spaced Shop"
        assert result.rows[0].address == "7 Rd"
