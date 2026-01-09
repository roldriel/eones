from datetime import datetime, timedelta, timezone

import pytest

from eones import add_days, format_date, from_timestamp, parse_date, to_timestamp
from eones.core.date import Date


def test_string_to_timestamp_to_string():
    date_str = "2025-07-11 10:30:00"
    dt = parse_date(date_str)
    ts = to_timestamp(dt)
    dt2 = from_timestamp(ts)
    final_str = format_date(dt2, fmt="%Y-%m-%d %H:%M:%S")
    assert final_str == date_str


def test_timestamp_and_add_days_consistency():
    d = parse_date("2025-07-11")
    ts = to_timestamp(d)
    d_from_ts = from_timestamp(ts)
    d_plus5 = add_days(d_from_ts, 5)
    d_expected = add_days(d, 5)
    assert d_plus5 == d_expected


def test_to_timestamp_returns_integer():
    d = parse_date("2025-07-11 10:30:00")
    ts = to_timestamp(d)
    assert isinstance(ts, int)


# Timezone-Aware DateTime Tests


def test_from_timezone_aware_datetime_comprehensive():
    """Test from_timezone_aware_datetime with various timezone types."""
    # Fixed offset positive (+05:30)
    offset_pos = timezone(timedelta(hours=5, minutes=30))
    dt = datetime(2024, 1, 1, 12, 0, tzinfo=offset_pos)
    d1 = Date.from_timezone_aware_datetime(dt)
    assert d1.year == 2024
    assert d1.hour == 12
    assert "UTC+05:30" in d1.timezone or d1.timezone == "UTC+05:30"

    # Fixed offset negative (-03:00)
    offset_neg = timezone(timedelta(hours=-3))
    dt2 = datetime(2024, 1, 1, 12, 0, tzinfo=offset_neg)
    d2 = Date.from_timezone_aware_datetime(dt2)
    assert d2.year == 2024
    assert "UTC-03" in d2.timezone or d2.timezone == "UTC-03"

    # timezone.utc
    from datetime import timezone as dt_timezone

    dt3 = datetime(2024, 1, 1, 12, 0, tzinfo=dt_timezone.utc)
    d3 = Date.from_timezone_aware_datetime(dt3)
    assert d3.timezone == "UTC"

    # Zero offset
    zero_offset = timezone(timedelta(0))
    dt4 = datetime(2024, 1, 1, 12, 0, tzinfo=zero_offset)
    d4 = Date.from_timezone_aware_datetime(dt4)
    assert d4.year == 2024


def test_from_timezone_aware_datetime_naive_error():
    """Test from_timezone_aware_datetime rejects naive datetime."""
    dt_naive = datetime(2024, 1, 1, 12, 0)
    with pytest.raises(ValueError, match="datetime must be timezone-aware"):
        Date.from_timezone_aware_datetime(dt_naive)
