from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones import Eones, InvalidFormatError, InvalidTimezoneError
from eones.core.date import Date
from eones.core.parser import Parser

# ==== FIXTURE ====


@pytest.fixture
def parser():
    return Parser(tz="UTC", formats=["%Y-%m-%d"])  # solo año-mes-día


def test_invalid_timezone_raises():
    with pytest.raises(InvalidTimezoneError):
        Parser(tz="Mars/Phobos")


# ==== VALID INPUTS ====


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (None, Date),
        (datetime(2025, 6, 15, 12, 0, tzinfo=ZoneInfo("UTC")), Date),
        ({"year": 2025, "month": 6, "day": 15}, Date),
    ],
)
def test_parse_valid_inputs(parser, value, expected_type):
    result = parser.parse(value)
    assert isinstance(result, expected_type)


def test_parse_existing_date_returns_same_instance(parser):
    d = Date(datetime(2025, 6, 15, tzinfo=ZoneInfo("UTC")), tz="UTC")
    result = parser.parse(d)
    assert result is d


# ==== INVALID INPUTS ====


@pytest.mark.parametrize(
    "invalid_input, exc", [(12345, ValueError), ("15/06/2025", InvalidFormatError)]
)
def test_parse_invalid_inputs_raise(parser, invalid_input, exc):
    with pytest.raises(exc):
        parser.parse(invalid_input)


@pytest.mark.parametrize(
    "invalid_dict",
    [
        {"year": 2025, "month": 13, "day": 32},  # fecha imposible
    ],
)
def test_from_dict_invalid_inputs_raise(parser, invalid_dict):
    with pytest.raises(ValueError):
        parser._from_dict(invalid_dict)


# ==== FROM DICT ====


def test_from_dict_valid_data(parser):
    result = parser._from_dict({"year": 2025, "month": 6, "day": 15})
    assert isinstance(result, Date)
    assert result.to_datetime().date().isoformat() == "2025-06-15"


def test_parse_dict_keeps_timezone():
    p = Parser(tz="America/Argentina/Buenos_Aires", formats=["%Y-%m-%d"])
    d = p.parse({"year": 2025, "month": 6, "day": 15})
    assert d.to_datetime().tzinfo.key == "America/Argentina/Buenos_Aires"


# ==== DEFAULT FORMATS ====


@pytest.mark.parametrize(
    "fmt, example",
    [
        ("%Y-%m-%d", "2025-06-15"),
        ("%d/%m/%Y", "15/06/2025"),
        ("%Y/%m/%d", "2025/06/15"),
        ("%d-%m-%Y", "15-06-2025"),
        ("%d.%m.%Y", "15.06.2025"),
        ("%Y-%m-%d %H:%M:%S", "2025-06-15 13:45:00"),
    ],
)
def test_default_formats_parsing(fmt, example):
    p = Parser(tz="UTC", formats=[fmt])
    result = p.parse(example).to_datetime()
    assert isinstance(result, datetime)
    assert result.year == 2025


# ==== MULTIPLE FORMATS ====


def test_multiple_formats_fallback_success():
    formats = ["%d/%m/%Y", "%Y-%m-%d"]
    p = Parser(tz="UTC", formats=formats)
    assert p.parse("2025-06-15").to_datetime().date().isoformat() == "2025-06-15"
    assert p.parse("15/06/2025").to_datetime().date().isoformat() == "2025-06-15"


def test_multiple_formats_fallback_failure():
    formats = ["%d/%m/%Y", "%Y-%m-%d"]
    p = Parser(tz="UTC", formats=formats)
    with pytest.raises(InvalidFormatError):
        p.parse("15.06.2025")  # no matching format


def test_from_dict_invalid_keys_raises():
    p = Parser(tz="UTC")
    with pytest.raises(ValueError, match="Invalid date part keys: .*"):
        p._from_dict({"year": 2024, "foo": 10})


def test_to_eones_date_with_date_instance():
    p = Parser(tz="UTC")
    d = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    result = p.to_eones_date(d)
    assert result is d


def test_to_eones_date_with_parseable_string():
    p = Parser(tz="UTC")
    result = p.to_eones_date("2024-01-01")
    assert isinstance(result, Date)


# ==== ISO 8601 PARSER TESTS ====


@pytest.fixture
def iso_parser():
    """Parser with default formats including ISO 8601 support."""
    return Parser(tz="UTC")


@pytest.fixture
def custom_tz_parser():
    """Parser with custom timezone."""
    return Parser(tz="America/New_York")


class TestParserIso8601:
    """Test Parser class with ISO 8601 formats."""

    @pytest.mark.parametrize(
        "iso_string",
        [
            "2024-01-15",
            "2024-01-15T10:30:00",
            "2024-01-15T10:30:00.123",
            "2024-01-15T10:30:00.123456",
            "2024-01-15T10:30:00Z",
            "2024-01-15T10:30:00.123Z",
            "2024-01-15T10:30:00.123456Z",
            "2024-01-15T10:30:00+00:00",
            "2024-01-15T10:30:00-00:00",
            "2024-01-15T10:30:00+03:00",
            "2024-01-15T10:30:00+05:30",
            "2024-01-15T10:30:00-05:00",
            "2024-01-15T10:30:00-08:00",
            "2024-01-15T10:30:00+0300",
            "2024-01-15T10:30:00-0500",
            "2024-01-15T10:30:00.123456+03:00",
            "2024-01-15T10:30:00.123456-05:00",
        ],
    )
    def test_parser_handles_iso_8601_formats(self, iso_parser, iso_string):
        """Test that parser can handle various ISO 8601 formats."""
        result = iso_parser.parse(iso_string)
        assert isinstance(result, Date)
        # Verify the date was parsed correctly
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parser_preserves_timezone_offsets(self, iso_parser):
        """Test that parser preserves timezone offsets from ISO strings."""
        # Test positive offset
        result_pos = iso_parser.parse("2024-01-15T10:30:00+03:00")
        assert "+03:00" in str(result_pos)

        # Test negative offset
        result_neg = iso_parser.parse("2024-01-15T10:30:00-05:00")
        assert "-05:00" in str(result_neg)

        # Test UTC
        result_utc = iso_parser.parse("2024-01-15T10:30:00Z")
        assert "+00:00" in str(result_utc)

    def test_parser_applies_default_timezone_to_naive_strings(self, custom_tz_parser):
        """Test that parser applies its default timezone to naive ISO strings."""
        result = custom_tz_parser.parse("2024-01-15T10:30:00")
        # Should use the parser's default timezone (America/New_York)
        assert (
            "America/New_York" in result.timezone
            or "EST" in result.timezone
            or "EDT" in result.timezone
        )

    def test_parser_default_formats_include_iso_8601(self, iso_parser):
        """Test that default formats include ISO 8601 patterns."""
        formats = iso_parser._formats
        # Check that ISO 8601 formats are included
        assert "%Y-%m-%dT%H:%M:%S" in formats
        assert "%Y-%m-%dT%H:%M:%S.%f" in formats
        assert "%Y-%m-%dT%H:%M:%SZ" in formats
        assert "%Y-%m-%dT%H:%M:%S%z" in formats
        assert "%Y-%m-%dT%H:%M:%S.%f%z" in formats

    @pytest.mark.parametrize(
        "invalid_iso",
        [
            "2024-13-15T10:30:00",  # Invalid month
            "2024-01-32T10:30:00",  # Invalid day
            "2024-01-15T25:30:00",  # Invalid hour
            "2024-01-15T10:60:00",  # Invalid minute
            "2024-01-15T10:30:60",  # Invalid second
            # Note: Invalid offset hours/minutes like +25:00 or +03:60 are
            # auto-corrected by Python 3.12+ fromisoformat and don't raise errors
        ],
    )
    def test_parser_handles_invalid_iso_strings(self, iso_parser, invalid_iso):
        """Test that parser properly handles invalid ISO 8601 strings."""
        with pytest.raises((ValueError, InvalidFormatError)):
            iso_parser.parse(invalid_iso)


# ==== PARSER COVERAGE IMPROVEMENTS TESTS ====


class TestParserCoverageImprovements:
    """Tests to cover uncovered lines in Parser class."""

    def test_parser_from_str_with_utc_timezone_name_precise(self):
        """Test Parser._from_str with UTC timezone name (line 127)."""
        from datetime import timedelta, tzinfo
        from unittest.mock import patch

        parser = Parser(formats=["%Y-%m-%d %H:%M:%S"])

        # Create a custom timezone that returns 'UTC' from tzname but isn't ZoneInfo
        class CustomUTCTZ(tzinfo):
            def tzname(self, dt):
                return "UTC"

            def utcoffset(self, dt):
                return timedelta(0)

        custom_utc_tz = CustomUTCTZ()
        dt_with_custom_utc = datetime(2024, 1, 1, 12, 0, 0, tzinfo=custom_utc_tz)

        # Mock strptime to return datetime with custom UTC timezone
        with patch("eones.core.parser.datetime") as mock_datetime:
            mock_datetime.strptime.return_value = dt_with_custom_utc

            date = parser._from_str("2024-01-01 12:00:00")
            assert date is not None

    def test_parser_from_str_with_offset_minutes_precise(self):
        """Test Parser._from_str with timezone offset having minutes (line 144)."""
        from datetime import timedelta, tzinfo
        from unittest.mock import patch

        parser = Parser(formats=["%Y-%m-%d %H:%M:%S"])

        # Create a custom timezone with non-zero minutes offset
        class CustomOffsetMinutesTZ(tzinfo):
            def tzname(self, dt):
                return "+0530"

            def utcoffset(self, dt):
                return timedelta(hours=5, minutes=30)

        custom_offset_tz = CustomOffsetMinutesTZ()
        dt_with_offset = datetime(2024, 1, 1, 12, 0, 0, tzinfo=custom_offset_tz)

        # Mock strptime to return datetime with custom offset timezone
        with patch("eones.core.parser.datetime") as mock_datetime:
            mock_datetime.strptime.return_value = dt_with_offset

            date = parser._from_str("2024-01-01 12:00:00")
            assert date is not None
