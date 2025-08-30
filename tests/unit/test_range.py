from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones import Eones
from eones.core.date import Date
from eones.core.delta import Delta
from eones.core.range import Range


def test_month_range():
    z = Date(datetime(2025, 6, 15, 14, 0, tzinfo=ZoneInfo("UTC")), tz="UTC")
    r = Range(z)
    start, end = r.month_range()

    assert start.day == 1
    assert end.day == 30
    assert start.hour == 0
    assert end.hour == 23
    assert end.minute == 59
    assert end.second == 59
    assert end.microsecond == 999999


def test_eones_range_invalid_mode():
    e = Eones("2025-01-01")
    with pytest.raises(ValueError, match="Invalid range mode"):
        e.range("decade")


def test_eonframe_repr():
    date = Date.from_iso("2025-01-01T00:00:00+00:00")
    frame = Range(date)
    result = repr(frame)
    assert result.startswith("Range(date=Date(")


def test_week_range():
    d = Date(datetime(2025, 6, 10, tzinfo=ZoneInfo("UTC")), tz="UTC")
    r = Range(d)
    start, end = r.week_range()

    assert start.weekday() == 0  # Monday
    assert end.weekday() == 6  # Sunday
    assert start.hour == 0 and start.minute == 0
    assert end.hour == 23 and end.minute == 59 and end.second == 59


def test_week_range_iso_standard():
    """Test week_range with ISO standard (Monday first)."""
    # Tuesday, June 10, 2025
    d = Date(datetime(2025, 6, 10, tzinfo=ZoneInfo("UTC")), tz="UTC")
    r = Range(d)
    start, end = r.week_range(first_day_of_week=0)  # ISO standard

    # Week should start on Monday (June 9) and end on Sunday (June 15)
    assert start.weekday() == 0  # Monday
    assert end.weekday() == 6  # Sunday
    assert start.day == 9  # June 9
    assert end.day == 15  # June 15
    assert start.hour == 0 and start.minute == 0
    assert end.hour == 23 and end.minute == 59 and end.second == 59


def test_week_range_us_standard():
    """Test week_range with US standard (Sunday first)."""
    # Tuesday, June 10, 2025
    d = Date(datetime(2025, 6, 10, tzinfo=ZoneInfo("UTC")), tz="UTC")
    r = Range(d)
    start, end = r.week_range(first_day_of_week=6)  # US standard

    # Week should start on Sunday (June 8) and end on Saturday (June 14)
    assert start.weekday() == 6  # Sunday
    assert end.weekday() == 5  # Saturday
    assert start.day == 8  # June 8
    assert end.day == 14  # June 14
    assert start.hour == 0 and start.minute == 0
    assert end.hour == 23 and end.minute == 59 and end.second == 59


@pytest.mark.parametrize(
    "test_date, first_day_of_week, expected_start_weekday, expected_end_weekday",
    [
        # ISO standard (Monday first)
        (
            datetime(2025, 6, 8, tzinfo=ZoneInfo("UTC")),
            0,
            0,
            6,
        ),  # Sunday -> Mon-Sun week
        (
            datetime(2025, 6, 9, tzinfo=ZoneInfo("UTC")),
            0,
            0,
            6,
        ),  # Monday -> Mon-Sun week
        (
            datetime(2025, 6, 14, tzinfo=ZoneInfo("UTC")),
            0,
            0,
            6,
        ),  # Saturday -> Mon-Sun week
        # US standard (Sunday first)
        (
            datetime(2025, 6, 8, tzinfo=ZoneInfo("UTC")),
            6,
            6,
            5,
        ),  # Sunday -> Sun-Sat week
        (
            datetime(2025, 6, 9, tzinfo=ZoneInfo("UTC")),
            6,
            6,
            5,
        ),  # Monday -> Sun-Sat week
        (
            datetime(2025, 6, 14, tzinfo=ZoneInfo("UTC")),
            6,
            6,
            5,
        ),  # Saturday -> Sun-Sat week
    ],
)
def test_week_range_parametrized(
    test_date, first_day_of_week, expected_start_weekday, expected_end_weekday
):
    """Test week_range with various dates and first day of week settings."""
    d = Date(test_date, tz="UTC")
    r = Range(d)
    start, end = r.week_range(first_day_of_week=first_day_of_week)

    assert start.weekday() == expected_start_weekday
    assert end.weekday() == expected_end_weekday
    assert start.hour == 0 and start.minute == 0
    assert end.hour == 23 and end.minute == 59 and end.second == 59


def test_quarter_range():
    d = Date(datetime(2025, 11, 15, tzinfo=ZoneInfo("UTC")), tz="UTC")
    r = Range(d)
    start, end = r.quarter_range()

    assert start.month == 10
    assert end.month == 12
    assert start.day == 1
    assert end.day == 31


def test_custom_range():
    base = Date(datetime(2025, 6, 15, 12, 0, tzinfo=ZoneInfo("UTC")), tz="UTC")
    r = Range(base)
    start_delta = Delta(months=-1)
    end_delta = Delta(months=1)
    start, end = r.custom_range(start_delta, end_delta)

    assert start.month == 5
    assert end.month == 7
    assert start.day == 15
    assert end.day == 15


# ==== Coverage Tests ====


def test_custom_range_invalid_types():
    """Test TypeError in custom_range (line 117)."""
    date = Date.now(tz="UTC", naive="utc")
    range_obj = Range(date)
    with pytest.raises(TypeError):
        range_obj.custom_range("not_a_delta", Delta(days=1))


def test_custom_range_swapped_order():
    """Test custom_range with end before start (line 122)."""
    date = Date.now(tz="UTC", naive="utc")
    range_obj = Range(date)
    start_delta = Delta(days=5)
    end_delta = Delta(days=1)
    start_dt, end_dt = range_obj.custom_range(start_delta, end_delta)
    # Should swap the order automatically
    assert start_dt <= end_dt
