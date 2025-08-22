from datetime import datetime, timedelta
from typing import cast
from zoneinfo import ZoneInfo

import pytest

from eones.core.date import Date
from eones.core.delta import Delta

# ==== Fixtures ====


@pytest.fixture
def friday():
    return Date(datetime(2025, 6, 13, tzinfo=ZoneInfo("UTC")))


@pytest.fixture
def dt_base():
    return datetime(2025, 6, 15, 12, 34, 56, 789000, tzinfo=ZoneInfo("UTC"))


# === Previous Weekday ===


@pytest.mark.parametrize(
    "start, target, expected_day",
    [
        (datetime(2025, 6, 13, tzinfo=ZoneInfo("UTC")), 0, 9),
        (datetime(2025, 6, 10, tzinfo=ZoneInfo("UTC")), 1, 3),
        (datetime(2025, 6, 12, tzinfo=ZoneInfo("UTC")), 2, 11),
    ],
)
def test_previous_weekday_variants(start, target, expected_day):
    d = Date(start, tz="UTC")
    prev = d.previous_weekday(target)
    assert prev.to_datetime().weekday() == target
    assert prev.to_datetime().day == expected_day


# ==== truncate / round ====


@pytest.mark.parametrize(
    "unit, expected",
    [
        ("second", datetime(2025, 6, 15, 12, 34, 56, tzinfo=ZoneInfo("UTC"))),
        ("minute", datetime(2025, 6, 15, 12, 34, 0, tzinfo=ZoneInfo("UTC"))),
        ("hour", datetime(2025, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC"))),
        ("day", datetime(2025, 6, 15, 0, 0, 0, tzinfo=ZoneInfo("UTC"))),
    ],
)
def test_truncate_exact(dt_base, unit, expected):
    d = Date(dt_base, tz="UTC")
    result = d.truncate(unit).to_datetime()
    assert result == expected


@pytest.mark.parametrize(
    "dt, unit, expected",
    [
        (datetime(2025, 6, 15, 12, 0, 35, tzinfo=ZoneInfo("UTC")), "minute", 1),
        (datetime(2025, 6, 15, 12, 0, 25, tzinfo=ZoneInfo("UTC")), "minute", 0),
        (datetime(2025, 6, 15, 12, 35, 0, tzinfo=ZoneInfo("UTC")), "hour", 13),
        (datetime(2025, 6, 15, 18, 0, 0, tzinfo=ZoneInfo("UTC")), "day", 16),
    ],
)
def test_round_variants(dt, unit, expected):
    d = Date(dt, tz="UTC")
    result = d.round(unit).to_datetime()
    assert getattr(result, unit) == expected


@pytest.mark.parametrize("invalid", ["invalid", "week", "month", "millisecond"])
def test_invalid_truncate_and_round(invalid):
    d = Date(datetime(2025, 6, 15, tzinfo=ZoneInfo("UTC")), tz="UTC")
    with pytest.raises(ValueError):
        d.truncate(invalid)
    with pytest.raises(ValueError):
        d.round(invalid)


# ==== to_datetime / to_iso / to_unix / from_unix ====


def test_to_datetime_identity():
    base = datetime(2025, 6, 15, 14, 30, tzinfo=ZoneInfo("UTC"))
    d = Date(base, tz="UTC")
    assert d.to_datetime() == base


def test_to_iso_returns_string():
    d = Date(datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC")))
    assert d.to_iso().startswith("2024-01-01T12:00")


def test_to_unix_returns_float():
    d = Date(datetime(1970, 1, 2, tzinfo=ZoneInfo("UTC")))
    assert isinstance(d.to_unix(), float)
    assert int(d.to_unix()) == 86400


def test_from_unix_creates_correct_date():
    d = Date.from_unix(86400, tz="UTC")
    assert d.year == 1970
    assert d.day == 2


# ==== __repr__ / __str__ ====


def test_repr_format():
    d = Date(datetime(2025, 6, 15, 10, 0, tzinfo=ZoneInfo("UTC")), tz="UTC")
    result = repr(d)
    assert isinstance(result, str)
    assert result.startswith("Date(")


def test_date_str_format():
    dt = Date(datetime(2024, 1, 1, 15, 30, tzinfo=ZoneInfo("UTC")))
    assert str(dt).startswith("2024-01-01T15:30")


# ==== Properties / Mutation ====


def test_date_component_properties():
    dt = Date(datetime(2024, 12, 31, 23, 59, 58, 999999, tzinfo=ZoneInfo("UTC")))
    assert dt.year == 2024
    assert dt.month == 12
    assert dt.day == 31
    assert dt.hour == 23
    assert dt.minute == 59
    assert dt.second == 58
    assert dt.microsecond == 999999


def test_date_replace_fields_returns_updated_date():
    d = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    new = d._replace_fields(month=12, day=25)
    assert new.month == 12
    assert new.day == 25
    assert isinstance(new, Date)


# ==== Shift / Add / Subtract ====


def test_date_shift_and_add_operator():
    d = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    shifted = d.shift(timedelta(days=5))
    added = d + timedelta(days=5)
    assert shifted.to_datetime().day == 6
    assert added.to_datetime().day == 6


def test_date_add_delta():
    d = Date(datetime(2024, 1, 31, tzinfo=ZoneInfo("UTC")))
    result = d + Delta(months=1)
    dt = result.to_datetime()
    assert dt.month == 2
    assert dt.day == 29


def test_date_subtract_timedelta():
    d = Date(datetime(2024, 1, 10, tzinfo=ZoneInfo("UTC")))
    result = d - timedelta(days=3)
    assert result.to_datetime().day == 7


def test_date_subtract_another_date():
    d1 = Date(datetime(2024, 1, 10, tzinfo=ZoneInfo("UTC")))
    d2 = Date(datetime(2024, 1, 5, tzinfo=ZoneInfo("UTC")))
    delta = d1 - d2
    assert delta.days == 5


def test_date_subtract_delta():
    d = Date(datetime(2024, 3, 31, tzinfo=ZoneInfo("UTC")))
    result = d - Delta(months=1)
    dt = result.to_datetime()
    assert dt.month == 2
    assert dt.day == 29


def test_date_sub_invalid_type_triggers_not_implemented():
    d = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    with pytest.raises(TypeError):
        _ = d - "2024-01-01"


# ==== Now / Timezones ====


def test_date_now_utc_has_utc_tz():
    d = Date.now(naive="utc")
    assert d.to_datetime().tzinfo.key == "UTC"


def test_date_now_local_has_local_tz():
    d = Date.now(naive="local")
    assert d.to_datetime().tzinfo is not None


def test_date_now_invalid_naive_raises():
    with pytest.raises(ValueError, match="Invalid 'naive' value"):
        Date.now(naive="invalid")


def test_date_naive_local_adds_local_tz():
    dt = datetime(2024, 1, 1, 12, 0)  # naive
    d = Date(dt, tz="UTC", naive="local")
    assert d.to_datetime().tzinfo is not None


def test_date_naive_utc_sets_utc_tz():
    dt = datetime(2024, 1, 1, 12, 0)  # naive
    d = Date(dt, tz="UTC", naive="utc")
    assert d.to_datetime().tzinfo.key == "UTC"


def test_date_naive_raises_without_tzinfo():
    with pytest.raises(ValueError, match="Naive datetime received"):
        Date(datetime(2024, 1, 1, 12, 0), tz="UTC", naive="raise")


def test_as_zone_changes_timezone():
    d = Date(datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC")))
    local_dt = d.as_zone("America/Argentina/Buenos_Aires")
    assert local_dt.tzinfo.key == "America/Argentina/Buenos_Aires"


def test_floor_week_sets_to_monday():
    d = Date(datetime(2024, 1, 4, tzinfo=ZoneInfo("UTC")))
    floored = d.floor("week")
    assert floored.to_datetime().weekday() == 0


def test_diff_invalid_unit_raises():
    d1 = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    d2 = Date(datetime(2024, 1, 2, tzinfo=ZoneInfo("UTC")))
    with pytest.raises(ValueError, match="Unsupported unit"):
        d1.diff(d2, unit="minutes")


def test_month_span_to_adjusts_for_day_difference():
    d1 = Date(datetime(2024, 1, 31, tzinfo=ZoneInfo("UTC")))
    d2 = Date(datetime(2024, 2, 28, tzinfo=ZoneInfo("UTC")))
    assert d1.month_span_to(d2) == 0


def test_year_span_to_adjusts_if_month_day_not_passed():
    d1 = Date(datetime(2020, 5, 20, tzinfo=ZoneInfo("UTC")))
    d2 = Date(datetime(2024, 5, 19, tzinfo=ZoneInfo("UTC")))
    assert d1.year_span_to(d2) == 3
    assert d2.year_span_to(d1) == -3


def test_to_dict_returns_all_fields():
    d = Date(datetime(2024, 1, 1, 12, 34, 56, 789000, tzinfo=ZoneInfo("UTC")))
    result = d.to_dict()
    assert result["year"] == 2024
    assert result["timezone"] == "UTC"


def test_rounded_invalid_unit_raises():
    d = Date(datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC")))
    with pytest.raises(ValueError, match="Invalid unit"):
        d._rounded(d.to_datetime(), unit="weeks")


def test_date_less_than_another():
    earlier = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    later = Date(datetime(2024, 1, 2, tzinfo=ZoneInfo("UTC")))
    assert earlier < later


def test_date_less_than_invalid_type():
    dt = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    with pytest.raises(TypeError):
        _ = dt < "2024-01-02"


def test_date_equality_with_another_date():
    dt1 = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    dt2 = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    assert dt1 == dt2


def test_date_equality_with_other_type():
    dt = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    assert (dt == "2024-01-01") is False


def test_date_hash():
    dt = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    assert isinstance(hash(dt), int)


@pytest.mark.parametrize(
    "unit, dt_kwargs, expected",
    [
        (
            "year",
            {"year": 2024, "month": 1, "day": 1},
            {"month": 12, "day": 31, "hour": 23, "minute": 59},
        ),
        (
            "month",
            {"year": 2024, "month": 4, "day": 1},
            {"day": 30, "hour": 23, "minute": 59},
        ),
        (
            "month",
            {"year": 2024, "month": 2, "day": 1},
            {"day": 29, "hour": 23, "minute": 59},
        ),
        (
            "week",
            {"year": 2024, "month": 4, "day": 1},
            {"weekday": 6, "hour": 23, "minute": 59},
        ),
        (
            "day",
            {"year": 2024, "month": 4, "day": 1, "hour": 10},
            {"hour": 23, "minute": 59, "second": 59},
        ),
        (
            "hour",
            {"year": 2024, "month": 4, "day": 1, "hour": 10},
            {"minute": 59, "second": 59},
        ),
        (
            "minute",
            {"year": 2024, "month": 4, "day": 1, "hour": 10, "minute": 25},
            {"second": 59},
        ),
        (
            "second",
            {
                "year": 2024,
                "month": 4,
                "day": 1,
                "hour": 10,
                "minute": 25,
                "second": 30,
            },
            {},
        ),
    ],
)
def test_ceil_units(unit, dt_kwargs, expected):
    base = Date(datetime(**dt_kwargs, tzinfo=ZoneInfo("UTC")))
    result = base.ceil(unit).to_datetime()
    assert isinstance(result, datetime)
    for attr, value in expected.items():
        if attr == "weekday":
            assert result.weekday() == value
        else:
            assert getattr(result, attr) == value

    assert result >= base.to_datetime()


@pytest.mark.parametrize("invalid_unit", ["millennium", "invalid", "siglo", "ms"])
def test_ceil_invalid_units_raise(invalid_unit):
    d = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    with pytest.raises(ValueError) as exc:
        d.ceil(invalid_unit)
    assert f"Unsupported unit: {invalid_unit}" in str(exc.value)


def test_constructor_invalid_naive_raises():
    dt = datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC"))
    with pytest.raises(ValueError, match="Invalid 'naive' value"):
        Date(dt, tz="UTC", naive="invalid")


def test_ceil_second_sets_microsecond():
    d = Date(datetime(2024, 1, 1, 12, 0, 0, 123456, tzinfo=ZoneInfo("UTC")))
    result = d.ceil("second").to_datetime()
    assert result.microsecond == 999999


def test_ceil_invalid_unit_only_in_ceil():
    d = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    d._dt = d._dt.replace(tzinfo=ZoneInfo("UTC"))
    with pytest.raises(ValueError, match="Unsupported unit: decade"):
        d.ceil("decade")


def test_ceil_final_else_branch_direct():
    class Dummy(Date):
        def floor(self, unit):
            return self

    d = Dummy(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    with pytest.raises(ValueError, match="Unsupported unit: fakeunit"):
        d.ceil("fakeunit")


def test_date_naive_unknown_mode_raises():
    dt = datetime(2024, 1, 1, 12, 0)
    with pytest.raises(ValueError, match="Invalid 'naive' value"):
        Date(dt, tz="UTC", naive="xyz")


def test_date_naive_raise_mode_without_tzinfo():
    dt = datetime(2024, 1, 1, 12, 0)  # naive
    with pytest.raises(ValueError, match="Naive datetime received"):
        Date(dt, tz="UTC", naive="raise")


@pytest.mark.parametrize(
    "method",
    [
        "start_of_day",
        "end_of_day",
        "start_of_month",
        "end_of_month",
        "start_of_year",
        "end_of_year",
    ],
)
def test_start_end_preserve_timezone(method):
    zone = "America/Argentina/Buenos_Aires"
    base = Date(datetime(2025, 6, 15, 12, 0, tzinfo=ZoneInfo(zone)), tz=zone)
    result = getattr(base, method)()
    assert result.to_datetime().tzinfo.key == zone


def test_is_same_day_true():
    d1 = Date(datetime(2024, 1, 1, 5, 0, tzinfo=ZoneInfo("UTC")))
    d2 = Date(datetime(2024, 1, 1, 23, 0, tzinfo=ZoneInfo("UTC")))
    assert d1.is_same_day(d2)


def test_is_same_day_false():
    d1 = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    d2 = Date(datetime(2024, 1, 2, tzinfo=ZoneInfo("UTC")))
    assert not d1.is_same_day(d2)


def test_is_before_and_is_after():
    earlier = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    later = Date(datetime(2024, 1, 2, tzinfo=ZoneInfo("UTC")))
    assert earlier.is_before(later)
    assert later.is_after(earlier)


def test_days_until():
    start = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")))
    end = Date(datetime(2024, 1, 5, tzinfo=ZoneInfo("UTC")))
    assert start.days_until(end) == 4
    assert end.days_until(start) == -4


def test_as_local_property():
    d = Date(datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC")))
    local_dt = d.as_local
    assert local_dt.tzinfo == datetime.now().astimezone().tzinfo


# ==== Coverage Tests ====


def test_invalid_timezone_in_init():
    """Test InvalidTimezoneError in Date.__init__ (lines 38-39)."""
    from eones.errors import InvalidTimezoneError
    with pytest.raises(InvalidTimezoneError):
        Date(tz="Invalid/Timezone")


def test_add_unsupported_type():
    """Test return NotImplemented in Date.__add__ (line 119)."""
    date = Date.now(tz="UTC", naive="utc")
    result = date.__add__("unsupported")
    assert result is NotImplemented


def test_from_iso_invalid_timezone():
    """Test InvalidTimezoneError in from_iso (lines 311-312)."""
    from eones.errors import InvalidTimezoneError
    # This test should trigger the ZoneInfoNotFoundError -> InvalidTimezoneError conversion
    # But since the exception is caught and re-raised as InvalidTimezoneError,
    # we need to create a scenario where ZoneInfo is actually called
    iso_str = "2024-01-01T12:00:00+00:00"  # ISO with timezone info
    with pytest.raises(InvalidTimezoneError):
        Date.from_iso(iso_str, tz="Invalid/Timezone")


def test_from_unix_invalid_timezone():
    """Test ZoneInfoNotFoundError in from_unix (lines 332-333)."""
    from eones.errors import InvalidTimezoneError
    with pytest.raises(InvalidTimezoneError):
        Date.from_unix(1640995200, tz="Invalid/Timezone")


def test_as_zone_invalid_timezone():
    """Test InvalidTimezoneError in as_zone (lines 427-428)."""
    from eones.errors import InvalidTimezoneError
    date = Date.now(tz="UTC", naive="utc")
    with pytest.raises(InvalidTimezoneError):
        date.as_zone("Invalid/Timezone")


def test_diff_for_humans_invalid_other_type():
    """Test TypeError in diff_for_humans (line 473)."""
    date = Date.now(tz="UTC", naive="utc")
    with pytest.raises(TypeError):
        date.diff_for_humans("invalid_type")


def test_end_of_month_december():
    """Test end_of_month with December (line 683)."""
    date = Date(datetime(2023, 12, 15), naive="utc")
    end_date = date.end_of_month()
    assert end_date.year == 2023
    assert end_date.month == 12
    assert end_date.day == 31
    assert end_date.hour == 23
    assert end_date.minute == 59
    assert end_date.second == 59
