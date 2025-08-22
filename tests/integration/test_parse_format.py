import pytest

from eones import format_date, parse_date


def test_parse_format_parse_round_trip():
    original = "2025-07-11"
    dt = parse_date(original)
    formatted = format_date(dt, fmt="%Y-%m-%d")
    dt2 = parse_date(formatted)
    assert dt == dt2


def test_parse_then_format_different_formats():
    dt = parse_date("2025-07-11 14:30:00")
    formatted1 = format_date(dt, fmt="%Y-%m-%d")
    formatted2 = format_date(dt, fmt="%d/%m/%Y")
    formatted3 = format_date(dt, fmt="%Y-%m-%d %H:%M:%S")

    assert formatted1 == "2025-07-11"
    assert formatted2 == "11/07/2025"
    assert formatted3 == "2025-07-11 14:30:00"


def test_parse_format_with_timezone_if_supported():
    date_str = "2025-07-11T14:30:00+00:00"
    dt = parse_date(date_str)
    formatted = format_date(dt, fmt="%Y-%m-%dT%H:%M:%S%z")
    assert formatted.startswith("2025-07-11T14:30:00")


def test_format_invalid_date_raises():
    with pytest.raises(TypeError):
        format_date("not a date object", "%Y-%m-%d")
