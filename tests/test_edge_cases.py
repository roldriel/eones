from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from eones.core.date import Date
from eones.core.delta import Delta


def test_leap_year_add_and_subtract():
    base = Date(datetime(2020, 2, 29, tzinfo=ZoneInfo("UTC")))
    plus_one = base + Delta(years=1)
    assert plus_one.to_datetime() == datetime(2021, 2, 28, tzinfo=ZoneInfo("UTC"))
    minus_one = plus_one - Delta(years=1)
    assert minus_one.to_datetime() == datetime(2020, 2, 28, tzinfo=ZoneInfo("UTC"))
    plus_four = base + Delta(years=4)
    assert plus_four.to_datetime() == datetime(2024, 2, 29, tzinfo=ZoneInfo("UTC"))


def test_dst_spring_forward_hour_skipped():
    zone = "America/New_York"
    dt = Date(datetime(2023, 3, 12, 1, 30, tzinfo=ZoneInfo(zone)), tz=zone)
    shifted = dt + timedelta(hours=1)
    result = shifted.to_datetime()
    assert result.hour == 2
    assert result.utcoffset().total_seconds() / 3600 == -5


def test_add_then_subtract_symmetry():
    base = Date(datetime(2024, 5, 15, 10, 0, tzinfo=ZoneInfo("UTC")))
    delta = Delta(days=3, hours=5)
    result = (base + delta) - delta
    assert result == base
