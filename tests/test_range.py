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
