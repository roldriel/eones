from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones import Eones
from eones.constants import DEFAULT_FORMATS
from eones.core.date import Date
from eones.core.parser import Parser

# ==== FIXTURE ====


@pytest.fixture
def parser():
    return Parser(tz="UTC", formats=["%Y-%m-%d"])  # solo año-mes-día


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


@pytest.mark.parametrize("invalid_input", [12345, "15/06/2025"])
def test_parse_invalid_inputs_raise(parser, invalid_input):
    with pytest.raises(ValueError):
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
    with pytest.raises(ValueError):
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
