"""No-pumping notice generator tests."""

from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from core.models import Organization

pytestmark = pytest.mark.django_db


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Pioneer Valley Septic")


def test_renders_letter_to_stdout(org):
    out = StringIO()
    call_command("no_pumping_notice", 2026, 2, stdout=out)

    text = out.getvalue()
    assert "February 2026" in text
    assert "NO septic pumping" in text
    assert "Pioneer Valley Septic" in text


def test_writes_letter_file(tmp_path):
    target = tmp_path / "notice.txt"

    call_command("no_pumping_notice", 2026, 3, town="Mendon", out=str(target), stdout=StringIO())

    body = target.read_text()
    assert "Board of Health\nMendon" in body
    assert "March 2026" in body


def test_bad_month_errors():
    with pytest.raises(CommandError):
        call_command("no_pumping_notice", 2026, 13, stdout=StringIO())
