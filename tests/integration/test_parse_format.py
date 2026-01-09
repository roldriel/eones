from datetime import datetime, timedelta, timezone

import pytest

from eones import format_date, parse_date
from eones.core.date import Date
from eones.core.parser import Parser


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


# ISO Parsing & Timezone Tests


def test_iso_parsing_comprehensive():
    """Test various ISO formats including edge cases and normalization."""
    # None tz defaults to UTC
    d1 = Date.from_iso("2024-01-01", tz=None)
    assert d1.timezone == "UTC"

    # Z suffix normalization
    d2 = Date.from_iso("2024-01-01T12:00:00Z", tz="UTC")
    assert d2.timezone == "UTC"

    # Z with microseconds
    d3 = Date.from_iso("2024-01-01T12:00:00.123456Z")
    assert d3.year == 2024

    # Offset without colon (+HHMM format)
    d4 = Date.from_iso("2024-01-01T12:00:00+0530")
    assert d4.year == 2024

    # Offset variations (+0000, -0500)
    d5 = Date.from_iso("2024-01-01T12:00:00+0000")
    assert d5.timezone == "UTC"
    d6 = Date.from_iso("2024-01-01T12:00:00-0500")
    assert d6.year == 2024

    # Naive datetime with custom timezone
    d7 = Date.from_iso("2024-01-01T12:00:00", tz="Europe/Madrid")
    assert "Europe/Madrid" in d7.timezone or "Madrid" in d7.timezone


def test_parser_custom_formats():
    """Test Parser with custom formats including timezone-aware."""
    p = Parser(tz="UTC", formats=["%Y/%m/%d %z"])
    d = p.parse("2024/01/01 +0200")
    assert d.year == 2024


def test_date_now_invalid_naive_parameter():
    """Test Date.now() with invalid naive parameter."""
    with pytest.raises(ValueError, match="Invalid 'naive' value"):
        Date.now(naive="invalid")
