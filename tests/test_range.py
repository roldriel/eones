from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones import Eones
from eones.core.date import Date
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
