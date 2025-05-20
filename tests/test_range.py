from datetime import datetime

import pytest

from eones import Eones
from eones.core.date import EonesDate
from eones.core.range import EonFrame


def test_month_range():
    z = EonesDate(datetime(2025, 6, 15, 14, 0), tz="UTC")
    r = EonFrame(z)
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
    date = EonesDate.from_iso("2025-01-01T00:00:00+00:00")
    frame = EonFrame(date)
    result = repr(frame)
    assert result.startswith("EonFrame(date=EonesDate(")
