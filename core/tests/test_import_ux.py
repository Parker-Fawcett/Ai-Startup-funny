"""Import UX pack: downloadable template, tolerant headers and dates."""

import io

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.importing import parse_customers_csv

pytestmark = pytest.mark.django_db


class TestTemplate:
    def test_template_downloads_with_sample_rows(self):
        response = Client().get(reverse("import_template"))
        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        body = response.content.decode()
        assert body.splitlines()[0].startswith("name,address")
        assert len(body.strip().splitlines()) >= 3  # header + samples


class TestHeaderTolerance:
    @pytest.mark.parametrize(
        "header",
        [
            "Customer Name,Street Address",
            "NAME , ADDRESS",
            "customer_name,street_address",
        ],
    )
    def test_aliased_and_sloppy_headers_map(self, header):
        result = parse_customers_csv(f"{header}\nDoe,1 Main St\n")
        assert [row.name for row in result.rows] == ["Doe"]
        assert not result.errors


class TestDateTolerance:
    @pytest.mark.parametrize("raw", ["2024-02-15", "02/15/2024", "2/5/2024"])
    def test_common_formats_parse(self, raw):
        result = parse_customers_csv(f"name,address,last_pumped\nA,1 Rd,{raw}\n")
        assert result.rows[0].last_pumped.isoformat() in {"2024-02-15", "2024-02-05"}
        assert not result.errors

    def test_garbage_date_still_rejected(self):
        result = parse_customers_csv("name,address,last_pumped\nA,1 Rd,whenever\n")
        assert result.errors[0].row_number == 2


class TestSuccessBanner:
    def test_full_import_redirects_with_count_message(self, client, org):

        _ = org
        c = Client()
        c.force_login(User.objects.create_superuser("ux", "ux@x.co", "pw12345!!"))

        csv_text = b"name,address\nA,1 Rd\nB,2 Rd\n"
        response = c.post(reverse("import"), {"csv_file": io.BytesIO(csv_text)}, follow=True)

        body = response.content.decode()
        assert "Imported 2 customers." in body
