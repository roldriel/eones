from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from eones import Eones
from eones.core.date import EonesDate

# ==== RANGE ====


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


# ==== IS_WITHIN ====


@pytest.mark.parametrize(
    "compare, expected, check_month",
    [
        ("2025-06-01", True, True),
        ({"year": 2025, "month": 6, "day": 1}, True, True),
        (datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC")), True, True),
        (EonesDate(datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC"))), True, True),
        (
            EonesDate(datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))),
            True,
            False,
        ),  # compara solo el año
    ],
)
def test_is_within_variants(compare, expected, check_month):
    z = Eones("2025-06-15", tz="UTC")
    assert z.is_within(compare, check_month=check_month) is expected


# ==== DIFFERENCE ====


@pytest.mark.parametrize(
    "a,b,unit,expected",
    [
        ("2025-05-10", "2025-05-15", "days", 5),
        ("2025-01-01", "2025-04-01", "months", 3),
        ("2020-01-01", "2025-01-01", "years", 5),
    ],
)
def test_difference_units(a, b, unit, expected):
    assert Eones(a).difference(Eones(b), unit=unit) == expected


def test_difference_with_string_input():
    a = Eones("2025-05-10")
    assert a.difference("2025-05-15", unit="days") == 5


def test_difference_invalid_unit_raises():
    a = Eones("2025-01-01")
    with pytest.raises(ValueError, match="Unsupported unit"):
        a.difference("2025-01-02", unit="hours")


@pytest.mark.parametrize(
    "b,expected",
    [
        (Eones("2025-01-04"), 3),
        (EonesDate(datetime(2025, 1, 5, tzinfo=timezone.utc)), 4),
        ("2025-01-05", 4),
    ],
)
def test_difference_with_varied_inputs(b, expected):
    a = Eones("2025-01-01")
    assert a.difference(b, unit="days") == expected


# ==== DATE OPERATIONS ====


def test_replace_date_parts():
    z = Eones("2025-05-15")
    z.replace(day=1, month=1)
    assert z.format("%Y-%m-%d") == "2025-01-01"


@pytest.mark.parametrize(
    "start,end,inclusive,expected",
    [
        ("2025-05-01", "2025-05-10", True, True),
        ("2025-05-01", "2025-05-09", True, False),
        ("2025-05-01", "2025-05-10", False, False),
        ("2025-05-01", "2025-05-11", False, True),
    ],
)
def test_is_between_cases(start, end, inclusive, expected):
    z = Eones("2025-05-10")
    assert z.is_between(start, end, inclusive=inclusive) is expected


@pytest.mark.parametrize(
    "other,expected",
    [
        ("2025-05-05", True),
        ("2025-05-12", False),
    ],
)
def test_is_same_week_cases(other, expected):
    z = Eones("2025-05-07")
    assert z.is_same_week(other) is expected


def test_next_weekday_returns_correct_day():
    z = Eones("2025-06-13")  # viernes
    next_monday = z.next_weekday(0)  # 0 = lunes
    assert next_monday.to_datetime().weekday() == 0
    assert next_monday.to_datetime().date() > z._date.to_datetime().date()


def test_now_returns_date_object():
    z = Eones("2025-05-15")
    current = z.now()
    assert isinstance(current, EonesDate)


def test_eones_repr():
    e = Eones("2025-01-01")
    assert "Eones(date=" in repr(e)


def test_eones_equality():
    a = Eones("2025-01-01")
    b = Eones("2025-01-01")
    c = Eones("2024-01-01")
    assert a == b
    assert a != c
    assert a != "not-an-eones"
