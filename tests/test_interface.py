from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones import Eones
from eones.core.date import Date

# ==== INIT ====


@pytest.mark.parametrize(
    "formats, additional_formats",
    [
        (["%Y-%m-%d"], ["%d-%m-%Y"]),
        ("%Y-%m-%d", ["%d-%m-%Y"]),
        (["%Y-%m-%d"], "%d-%m-%Y"),
        ("%Y-%m-%d", "%d-%m-%Y"),
    ],
)
def test_eones_init_mutual_exclusion_raises(formats, additional_formats):
    with pytest.raises(
        ValueError, match="Use either 'formats' or 'additional_formats'"
    ):
        Eones("2024-01-01", formats=formats, additional_formats=additional_formats)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"formats": "%Y-%m-%d"},
        {"additional_formats": "%Y-%m-%d"},
        {"additional_formats": ["%Y-%m-%d"]},
    ],
)
def test_eones_init_format_variants(kwargs):
    e = Eones("2024-01-01", **kwargs)
    assert isinstance(e, Eones)


# ==== REPRESENTATION & COMPARISON ====


def test_eones_repr_contains_date_and_tz():
    e = Eones("2025-06-15T14:30:00", tz="UTC")
    representation = repr(e)
    assert "Eones(date=" in representation
    assert "tz='UTC'" in representation


def test_eones_equality_same_value():
    a = Eones("2024-01-01", tz="UTC")
    b = Eones("2024-01-01", tz="UTC")
    assert a == b


def test_eones_equality_not_instance():
    a = Eones("2024-01-01", tz="UTC")
    assert a != "2024-01-01"


# ==== TIME TRANSFORMATIONS ====


@pytest.mark.parametrize(
    "method, unit",
    [
        ("floor", "hour"),
        ("ceil", "hour"),
        ("round", "day"),
        ("start_of", "month"),
        ("end_of", "month"),
    ],
)
def test_eones_unit_transformations(method, unit):
    e = Eones("2024-03-17T15:45:23")
    transformed = getattr(e, method)(unit)
    assert isinstance(transformed, Eones)


def test_replace_method_changes_date_fields():
    e = Eones("2024-01-15", tz="UTC")
    result = e.replace(month=12, day=25)
    assert isinstance(result, Eones)
    dt = result.now().to_datetime()
    assert dt.month == 12
    assert dt.day == 25


def test_next_weekday_returns_correct_type():
    e = Eones("2025-01-01", tz="UTC")
    result = e.next_weekday(4)
    assert isinstance(result, Date)


# ==== RANGE & POSITIONAL CHECKS ====


@pytest.mark.parametrize(
    "mode, check",
    [
        ("day", lambda s, e: s.hour == 0 and e.hour == 23),
        ("month", lambda s, e: s.day == 1 and e.day == 30),
        ("year", lambda s, e: s.month == 1 and e.day == 31),
    ],
)
def test_eones_range_modes(mode, check):
    z = Eones("2025-06-15", tz="UTC")
    start, end = z.range(mode)
    assert check(start, end)


def test_eones_range_invalid_mode_raises():
    z = Eones("2025-06-15", tz="UTC")
    with pytest.raises(ValueError, match="Invalid range mode"):
        z.range("decade")


@pytest.mark.parametrize(
    "compare, expected, check_month",
    [
        ("2025-06-01", True, True),
        ({"year": 2025, "month": 6, "day": 1}, True, True),
        (datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC")), True, True),
        (Date(datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC"))), True, True),
        (Date(datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))), True, False),
    ],
)
def test_is_within_variants(compare, expected, check_month):
    z = Eones("2025-06-15", tz="UTC")
    assert z.is_within(compare, check_month=check_month) is expected


def test_is_between_inclusive_true():
    e = Eones("2025-01-15", tz="UTC")
    assert e.is_between("2025-01-01", "2025-01-31", inclusive=True) is True


def test_is_between_inclusive_false_outside():
    e = Eones("2025-01-01", tz="UTC")
    assert e.is_between("2025-01-01", "2025-01-15", inclusive=False) is False


def test_is_same_week_with_eones_instance():
    e1 = Eones("2024-01-01")
    e2 = Eones("2024-01-02")
    assert e1.is_same_week(e2) is True


def test_is_same_week_with_datetime_input():
    dt = datetime(2025, 1, 2, tzinfo=ZoneInfo("UTC"))
    e = Eones("2025-01-01", tz="UTC")
    assert e.is_same_week(dt) is True


# ==== DIFFERENCE ====


@pytest.mark.parametrize(
    "a,b,unit,expected",
    [
        ("2024-01-01", "2024-01-03", "days", 2),
        ("2024-01-01", "2024-01-15", "weeks", 2),
        ("2024-01-01", "2024-04-01", "months", 3),
        ("2022-01-01", "2024-01-01", "years", 2),
    ],
)
def test_difference_units(a, b, unit, expected):
    z = Eones(a)
    result = z.difference(b, unit=unit)
    assert result == expected


def test_difference_with_eones_instance():
    a = Eones("2025-01-01", tz="UTC")
    b = Eones("2025-01-15", tz="UTC")
    assert a.difference(b, unit="days") == 14


def test_difference_with_date_instance():
    dt = datetime(2025, 1, 15, tzinfo=ZoneInfo("UTC"))
    d = Date(dt)
    e = Eones("2025-01-01", tz="UTC")
    assert e.difference(d, unit="days") == 14


def test_coerce_to_date_from_eones():
    a = Eones("2024-01-01", tz="UTC")
    b = Eones("2024-01-15", tz="UTC")
    assert a._coerce_to_date(b).to_datetime().day == 15


def test_coerce_to_date_accepts_eones_instance():
    a = Eones("2024-01-01", tz="UTC")
    b = Eones("2024-01-15", tz="UTC")
    coerced = a._coerce_to_date(b)
    assert isinstance(coerced, Date)
    assert coerced.to_datetime().day == 15


def test_diff_for_humans_english_and_spanish():
    start = Eones("2025-01-10", tz="UTC")
    end = Eones("2025-01-17", tz="UTC")

    assert start.diff_for_humans(end, locale="en") == "1 week ago"
    assert end.diff_for_humans(start, locale="en") == "in 1 week"

    assert start.diff_for_humans(end, locale="es") == "hace 1 semana"
    assert end.diff_for_humans(start, locale="es") == "en 1 semana"
