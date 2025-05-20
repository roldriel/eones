from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from eones.core.date import EonesDate

# ==== FIXTURES ====


@pytest.fixture
def june_15():
    return EonesDate(datetime(2025, 6, 15, 12, 34, 56), tz="UTC")


@pytest.fixture
def friday():
    return EonesDate(datetime(2025, 6, 13), tz="UTC")


# ==== BASIC FUNCTIONALITY ====


def test_previous_weekday_monday_from_friday(friday):
    prev = friday.previous_weekday(0)  # Monday
    assert prev.to_datetime().weekday() == 0
    assert prev.to_datetime().day == 9


@pytest.mark.parametrize(
    "unit, attr",
    [
        ("second", "microsecond"),
        ("minute", "second"),
        ("hour", "minute"),
        ("day", "hour"),
    ],
)
def test_truncate_variants(june_15, unit, attr):
    result = june_15.truncate(unit)
    assert getattr(result.to_datetime(), attr) == 0


@pytest.mark.parametrize(
    "dt, unit, expected",
    [
        (
            datetime(2025, 6, 15, 12, 0, 35, tzinfo=ZoneInfo("UTC")),
            "minute",
            1,
        ),  # 12:00:35 → 12:01
        (
            datetime(2025, 6, 15, 12, 35, 0, tzinfo=ZoneInfo("UTC")),
            "hour",
            13,
        ),  # 12:35:00 → 13:00
        (
            datetime(2025, 6, 15, 18, 0, 0, tzinfo=ZoneInfo("UTC")),
            "day",
            16,
        ),  # 18:00:00 → 00:00 of next day
    ],
)
def test_round_variants(dt, unit, expected):
    d = EonesDate(dt, tz="UTC")
    result = d.round(unit).to_datetime()
    assert getattr(result, unit) == expected


@pytest.mark.parametrize("invalid", ["invalid", "week", "month", "millisecond"])
def test_invalid_truncate_and_round(invalid):
    d = EonesDate(datetime(2025, 6, 15), tz="UTC")
    with pytest.raises(ValueError):
        d.truncate(invalid)
    with pytest.raises(ValueError):
        d.round(invalid)


def test_repr_format():
    d = EonesDate(datetime(2025, 6, 15, 10, 0), tz="UTC")
    result = repr(d)
    assert isinstance(result, str)
    assert result.startswith("EonesDate(")


def test_is_within_logic():
    z1 = EonesDate(datetime(2025, 6, 15))
    z2 = EonesDate(datetime(2025, 6, 1))
    z3 = EonesDate(datetime(2025, 5, 1))
    z4 = EonesDate(datetime(2024, 6, 1))
    z5 = EonesDate(datetime(2025, 1, 1))

    assert z1.is_within(z2)
    assert not z1.is_within(z3)
    assert not z1.is_within(z4)
    assert z1.is_within(z5, check_month=False)


def test_comparison_operators():
    d1 = EonesDate(datetime(2025, 6, 15))
    d2 = EonesDate(datetime(2025, 6, 16))
    assert d1 < d2
    assert not d2 < d1
    assert (d1 == "2025-06-15") is False
    assert (d1 == d2) is False


def test_diff_methods_direct():
    d1 = EonesDate(datetime(2025, 6, 15))
    d2 = EonesDate(datetime(2025, 6, 10))
    d3 = EonesDate(datetime(2020, 1, 1))
    d4 = EonesDate(datetime(2024, 2, 1))

    assert d1.diff(d2, unit="days") == 5
    assert d1.diff(d3, unit="years") == 5
    assert d1.diff(d4, unit="months") == 16


def test_replace_fields():
    d = EonesDate(datetime(2025, 6, 15, 10, 30), tz="UTC")
    d2 = d.replace(year=2024, month=1, day=1, hour=0, minute=0, second=0)
    dt = d2.to_datetime()
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) == (
        2024,
        1,
        1,
        0,
        0,
        0,
    )


def test_start_and_end_periods():
    d = EonesDate(datetime(2025, 6, 15, 10, 30), tz="UTC")
    assert d.start_of("month").day == 1
    assert d.start_of("year").month == 1
    assert d.end_of("month").day == 30
    assert d.end_of("year").month == 12
    assert d.end_of("year").day == 31


def test_start_end_of_week():
    d = EonesDate(datetime(2025, 6, 13), tz="UTC")  # Friday
    assert d.start_of("week").weekday() == 0
    assert d.end_of("week").weekday() == 6


def test_start_end_invalid_period():
    d = EonesDate(datetime(2025, 6, 15), tz="UTC")
    with pytest.raises(ValueError):
        d.start_of("decade")
    with pytest.raises(ValueError):
        d.end_of("century")


def test_iso_and_unix_conversion():
    d = EonesDate(datetime(2025, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
    assert "2025-06-15T12:00:00" in d.to_iso()
    assert isinstance(d.to_unix(), float)

    ts = d.to_unix()
    restored = EonesDate.from_unix(ts)
    assert restored.to_datetime() == d.to_datetime()


def test_start_end_of_day():
    d = EonesDate(datetime(2025, 6, 15, 12, 34, 56), tz="UTC")
    start = d.start_of("day")
    end = d.end_of("day")
    assert (start.hour, start.minute, start.second, start.microsecond) == (0, 0, 0, 0)
    assert (end.hour, end.minute, end.second, end.microsecond) == (23, 59, 59, 999999)


def test_is_same_week():
    d1 = EonesDate(datetime(2025, 6, 10), tz="UTC")
    d2 = EonesDate(datetime(2025, 6, 13), tz="UTC")
    d3 = EonesDate(datetime(2025, 6, 17), tz="UTC")
    assert d1.is_same_week(d2)
    assert not d1.is_same_week(d3)


def test_copy_and_equality():
    d1 = EonesDate(datetime(2025, 6, 15, 12, 0), tz="UTC")
    d2 = d1.copy()
    assert d1.to_datetime() == d2.to_datetime()
    assert d1 is not d2


def test_as_utc_conversion():
    d = EonesDate(datetime(2025, 6, 15, 12, 0), tz="America/Argentina/Buenos_Aires")
    utc = d.as_utc()
    assert utc.tzinfo == timezone.utc


def test_as_local_conversion():
    d = EonesDate(datetime(2025, 6, 15, 12, 0), tz="UTC")
    local = d.as_local("America/Argentina/Buenos_Aires")
    assert local.tzinfo.key == "America/Argentina/Buenos_Aires"


def test_from_iso_without_timezone():
    iso_str = "2025-06-15T12:00:00"
    z = EonesDate.from_iso(iso_str, tz="UTC")
    assert z.to_datetime().hour == 12
    assert z.to_datetime().tzinfo is not None


def test_eonesdate_hash():
    d = EonesDate.from_iso("2025-01-01")
    assert isinstance(hash(d), int)


def test_eonesdate_delegated_attribute():
    d = EonesDate.from_iso("2025-01-01")
    assert d.year == 2025


def test_eonesdate_str():
    d = EonesDate.from_iso("2025-01-01")
    assert "2025-01-01" in str(d)


def test_eonesdate_eq_with_datetime():
    dt = datetime(2025, 6, 15, tzinfo=timezone.utc)
    ed = EonesDate(dt)
    assert ed == dt
