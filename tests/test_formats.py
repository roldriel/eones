from eones import Eones
from eones.formats import is_valid_format, sanitize_formats


def test_is_valid_format_success():
    formats = ["%Y-%m-%d", "%d/%m/%Y"]
    assert is_valid_format("2025-06-15", formats)
    assert is_valid_format("15/06/2025", formats)


def test_is_valid_format_failure():
    formats = ["%Y-%m-%d"]
    assert not is_valid_format("15-06-2025", formats)


def test_sanitize_formats():
    formats = ["%Y-%m-%d", "%Y-%m-%d", "%d/%m/%Y", 123, None]
    result = sanitize_formats(formats)
    assert "%Y-%m-%d" in result
    assert "%d/%m/%Y" in result
    assert all(isinstance(fmt, str) for fmt in result)


def test_add_days_to_date():
    z = Eones("2025-05-15")
    z.add(days=5)
    assert z.format("%Y-%m-%d") == "2025-05-20"


def test_add_months_to_date():
    z = Eones("2025-01-31")
    z.add(months=1)
    assert z.format("%Y-%m-%d") == "2025-02-28"  # manejo de mes corto


def test_format_date():
    z = Eones("2025-12-24")
    formatted = z.format("%d/%m/%Y")
    assert formatted == "24/12/2025"
