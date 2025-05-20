from datetime import datetime

import pytest

from eones.constants import DEFAULT_FORMATS
from eones.core.date import EonesDate
from eones.core.parser import Chronologer


@pytest.fixture
def parser():
    return Chronologer(tz="UTC", formats=["%Y-%m-%d"])  # solo año-mes-día


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (None, EonesDate),
        (datetime(2025, 6, 15, 12, 0), EonesDate),
        ({"year": 2025, "month": 6, "day": 15}, EonesDate),
    ],
)
def test_parse_valid_inputs(parser, value, expected_type):
    result = parser.parse(value)
    assert isinstance(result, expected_type)
    if value and isinstance(value, (datetime, dict)):
        assert result.to_datetime().date().isoformat() == "2025-06-15"


def test_parse_existing_eonesdate_returns_same(parser):
    d = EonesDate(datetime(2025, 6, 15), tz="UTC")
    result = parser.parse(d)
    assert result is d


@pytest.mark.parametrize("invalid_input", [12345, "15/06/2025"])
def test_parse_invalid_inputs_raise(parser, invalid_input):
    with pytest.raises(ValueError):
        parser.parse(invalid_input)


@pytest.mark.parametrize(
    "invalid_dict",
    [
        {"year": "not-a-number", "month": 6},
        {"year": 2025, "month": "junio"},
        {"year": 2025, "month": 13, "day": 32},
    ],
)
def test_from_dict_invalid_inputs_raise(parser, invalid_dict):
    with pytest.raises(ValueError):
        parser._from_dict(invalid_dict)


def test_from_dict_valid_data(parser):
    result = parser._from_dict({"year": 2025, "month": 6, "day": 15})
    assert isinstance(result, EonesDate)
    assert result.to_datetime().date().isoformat() == "2025-06-15"


# Test que valida que todos los formatos de DEFAULT_FORMATS se parsean correctamente
@pytest.mark.parametrize(
    "fmt, example",
    [
        ("%Y-%m-%d", "2025-06-15"),
        ("%d/%m/%Y", "15/06/2025"),
        ("%Y/%m/%d", "2025/06/15"),
        ("%d-%m-%Y", "15-06-2025"),
        ("%d.%m.%Y", "15.06.2025"),
        ("%Y-%m-%d %H:%M:%S", "2025-06-15 13:45:00"),
        ("%d/%m/%Y %H:%M:%S", "15/06/2025 13:45:00"),
        ("%Y-%m-%dT%H:%M:%S", "2025-06-15T13:45:00"),
        ("%Y-%m-%dT%H:%M", "2025-06-15T13:45"),
        ("%Y-%m-%d %H:%M", "2025-06-15 13:45"),
        ("%d %b %Y", "15 Jun 2025"),
        ("%d %B %Y", "15 June 2025"),
        ("%Y%m%d", "20250615"),
        ("%d%m%Y", "15062025"),
        ("%Y-%m-%dT%H:%M:%S.%f", "2025-06-15T13:45:00.000000"),
        ("%Y-%m-%dT%H:%M:%S.%fZ", "2025-06-15T13:45:00.000000Z"),
        ("%a %b %d %H:%M:%S %Y", "Sun Jun 15 13:45:00 2025"),
    ],
)
def test_default_formats_are_parsable(fmt, example):
    parser = Chronologer(tz="UTC", formats=[fmt])
    result = parser.parse(example)
    assert isinstance(result, EonesDate)
    assert result.to_datetime().year == 2025
    assert result.to_datetime().month == 6
    assert result.to_datetime().day == 15
