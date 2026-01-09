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
    """Test InvalidTimezoneError in from_iso when tz parameter is invalid."""
    from eones.errors import InvalidTimezoneError

    # Use ISO string without timezone info so the tz parameter is actually used
    iso_str = "2024-01-01T12:00:00"  # ISO without timezone info
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


# ==== Semantic Calendar Methods Tests ====


@pytest.mark.parametrize(
    "year, expected",
    [
        (2020, True),  # Divisible by 4 and 400
        (2021, False),  # Not divisible by 4
        (2000, True),  # Divisible by 400
        (1900, False),  # Divisible by 100 but not 400
        (2024, True),  # Divisible by 4 but not 100
        (1996, True),  # Divisible by 4 but not 100
        (1800, False),  # Divisible by 100 but not 400
    ],
)
def test_is_leap_year(year, expected):
    """Test is_leap_year method with various years."""
    date = Date(datetime(year, 6, 15), naive="utc")
    assert date.is_leap_year() == expected


@pytest.mark.parametrize(
    "weekday, expected",
    [
        (0, False),  # Monday
        (1, False),  # Tuesday
        (2, False),  # Wednesday
        (3, False),  # Thursday
        (4, False),  # Friday
        (5, True),  # Saturday
        (6, True),  # Sunday
    ],
)
def test_is_weekend(weekday, expected):
    """Test is_weekend method with different weekdays."""
    # Create a date for each weekday (2024-01-01 is Monday)
    base_date = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))  # Monday
    target_date = base_date + timedelta(days=weekday)
    date = Date(target_date)
    assert date.is_weekend() == expected


@pytest.mark.parametrize(
    "weekday, method_name, expected",
    [
        (0, "is_monday", True),
        (1, "is_monday", False),
        (0, "is_tuesday", False),
        (1, "is_tuesday", True),
        (2, "is_wednesday", True),
        (3, "is_wednesday", False),
        (3, "is_thursday", True),
        (4, "is_thursday", False),
        (4, "is_friday", True),
        (5, "is_friday", False),
        (5, "is_saturday", True),
        (6, "is_saturday", False),
        (6, "is_sunday", True),
        (0, "is_sunday", False),
    ],
)
def test_weekday_methods(weekday, method_name, expected):
    """Test individual weekday methods (is_monday, is_tuesday, etc.)."""
    # Create a date for each weekday (2024-01-01 is Monday)
    base_date = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))  # Monday
    target_date = base_date + timedelta(days=weekday)
    date = Date(target_date)
    method = getattr(date, method_name)
    assert method() == expected


def test_semantic_methods_integration():
    """Test integration of semantic methods with real dates."""
    # Test with a known leap year Saturday
    leap_saturday = Date(datetime(2024, 2, 10), naive="utc")  # Saturday in leap year
    assert leap_saturday.is_leap_year() is True
    assert leap_saturday.is_weekend() is True
    assert leap_saturday.is_saturday() is True
    assert leap_saturday.is_sunday() is False

    # Test with a non-leap year weekday
    non_leap_tuesday = Date(
        datetime(2023, 3, 14), naive="utc"
    )  # Tuesday in non-leap year
    assert non_leap_tuesday.is_leap_year() is False
    assert non_leap_tuesday.is_weekend() is False
    assert non_leap_tuesday.is_tuesday() is True
    assert non_leap_tuesday.is_monday() is False


@pytest.mark.parametrize(
    "weekday, first_day_of_week, expected",
    [
        # ISO standard (Monday first) - Saturday and Sunday are weekend
        (5, 0, True),  # Saturday
        (6, 0, True),  # Sunday
        (0, 0, False),  # Monday
        (4, 0, False),  # Friday
        # US standard (Sunday first) - Friday and Saturday are weekend
        (5, 6, True),  # Saturday
        (4, 6, True),  # Friday
        (6, 6, False),  # Sunday
        (0, 6, False),  # Monday
    ],
)
def test_is_weekend_with_first_day_config(weekday, first_day_of_week, expected):
    """Test is_weekend() with different first day of week configurations."""
    # Create a date for each weekday (2024-01-01 is Monday)
    base_date = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))  # Monday
    target_date = base_date + timedelta(days=weekday)
    date = Date(target_date)

    # Test the is_weekend_day function directly with different configurations
    from eones.constants import is_weekend_day

    result = is_weekend_day(date._dt.weekday(), first_day_of_week)
    assert result == expected


def test_is_weekend_default_iso_behavior():
    """Test that is_weekend() uses ISO standard by default."""
    # Saturday should be weekend
    saturday = Date(datetime(2024, 1, 6), naive="utc")  # Saturday
    assert saturday.is_weekend() is True

    # Sunday should be weekend
    sunday = Date(datetime(2024, 1, 7), naive="utc")  # Sunday
    assert sunday.is_weekend() is True

    # Friday should not be weekend
    friday = Date(datetime(2024, 1, 5), naive="utc")  # Friday
    assert friday.is_weekend() is False


# ==== ISO 8601 PARSING TESTS ====


class TestDateFromIso:
    """Test Date.from_iso() method with various ISO 8601 formats."""

    @pytest.mark.parametrize(
        "iso_string, expected_offset",
        [
            # Basic formats without timezone
            ("2024-01-15", "+00:00"),
            ("2024-01-15T10:30:00", "+00:00"),
            ("2024-01-15T10:30:00.123", "+00:00"),
            ("2024-01-15T10:30:00.123456", "+00:00"),
            # UTC formats
            ("2024-01-15T10:30:00Z", "+00:00"),
            ("2024-01-15T10:30:00.123Z", "+00:00"),
            ("2024-01-15T10:30:00.123456Z", "+00:00"),
            # Zero offset formats
            ("2024-01-15T10:30:00+00:00", "+00:00"),
            ("2024-01-15T10:30:00-00:00", "+00:00"),
            # Positive offsets with colon
            ("2024-01-15T10:30:00+03:00", "+03:00"),
            ("2024-01-15T10:30:00+05:30", "+05:30"),
            ("2024-01-15T10:30:00+09:00", "+09:00"),
            ("2024-01-15T10:30:00+12:00", "+12:00"),
            # Negative offsets with colon
            ("2024-01-15T10:30:00-05:00", "-05:00"),
            ("2024-01-15T10:30:00-08:00", "-08:00"),
            ("2024-01-15T10:30:00-03:30", "-03:30"),
            ("2024-01-15T10:30:00-11:00", "-11:00"),
            # Offsets without colon
            ("2024-01-15T10:30:00+0300", "+03:00"),
            ("2024-01-15T10:30:00-0500", "-05:00"),
            ("2024-01-15T10:30:00+0000", "+00:00"),
            # With microseconds and offsets
            ("2024-01-15T10:30:00.123456+03:00", "+03:00"),
            ("2024-01-15T10:30:00.123456-05:00", "-05:00"),
        ],
    )
    def test_from_iso_preserves_timezone_offset(self, iso_string, expected_offset):
        """Test that from_iso preserves timezone offsets correctly."""
        date = Date.from_iso(iso_string)
        assert str(date).endswith(expected_offset)

    @pytest.mark.parametrize(
        "iso_string, expected_year, expected_month, expected_day, expected_hour, expected_minute",
        [
            ("2024-01-15", 2024, 1, 15, 0, 0),
            ("2024-12-31T23:59:59+05:30", 2024, 12, 31, 23, 59),
            ("2023-06-15T14:30:45-08:00", 2023, 6, 15, 14, 30),
            ("2025-03-10T08:15:30.123456Z", 2025, 3, 10, 8, 15),
        ],
    )
    def test_from_iso_parses_datetime_components_correctly(
        self,
        iso_string,
        expected_year,
        expected_month,
        expected_day,
        expected_hour,
        expected_minute,
    ):
        """Test that datetime components are parsed correctly."""
        date = Date.from_iso(iso_string)
        dt = date.to_datetime()
        assert dt.year == expected_year
        assert dt.month == expected_month
        assert dt.day == expected_day
        assert dt.hour == expected_hour
        assert dt.minute == expected_minute

    def test_from_iso_with_custom_timezone_for_naive_strings(self):
        """Test that custom timezone is applied to naive ISO strings."""
        date = Date.from_iso("2024-01-15T10:30:00", tz="America/New_York")
        # Should have New York timezone for naive string
        assert (
            "America/New_York" in date.timezone
            or "EST" in date.timezone
            or "EDT" in date.timezone
        )

    def test_from_iso_preserves_existing_timezone_info(self):
        """Test that existing timezone info in ISO string is preserved."""
        date = Date.from_iso("2024-01-15T10:30:00+03:00", tz="America/New_York")
        # Should preserve the +03:00 offset, not use New York timezone
        assert "+03:00" in str(date)


class TestIso8601EdgeCases:
    """Test edge cases for ISO 8601 parsing."""

    def test_leap_year_february_29(self):
        """Test parsing February 29 in leap years."""
        # 2024 is a leap year
        date = Date.from_iso("2024-02-29T12:00:00+00:00")
        assert date.month == 2
        assert date.day == 29
        assert date.year == 2024

    def test_end_of_year_with_timezone(self):
        """Test parsing end of year with timezone offset."""
        date = Date.from_iso("2024-12-31T23:59:59.999999+14:00")
        assert date.year == 2024
        assert date.month == 12
        assert date.day == 31
        assert "+14:00" in str(date)

    def test_beginning_of_year_with_negative_timezone(self):
        """Test parsing beginning of year with negative timezone offset."""
        date = Date.from_iso("2024-01-01T00:00:00.000000-12:00")
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 1
        assert "-12:00" in str(date)

    @pytest.mark.parametrize(
        "offset_format, expected_offset",
        [
            ("+0000", "+00:00"),
            ("-0000", "+00:00"),
            ("+0100", "+01:00"),
            ("-0100", "-01:00"),
            ("+1400", "+14:00"),
            ("-1200", "-12:00"),
        ],
    )
    def test_offset_format_normalization(self, offset_format, expected_offset):
        """Test that different offset formats are normalized correctly."""
        iso_string = f"2024-01-15T10:30:00{offset_format}"
        date = Date.from_iso(iso_string)
        assert expected_offset in str(date)

    def test_microseconds_precision_preservation(self):
        """Test that microseconds precision is preserved."""
        date = Date.from_iso("2024-01-15T10:30:00.123456+03:00")
        dt = date.to_datetime()
        assert dt.microsecond == 123456

    def test_timezone_name_generation_for_fixed_offsets(self):
        """Test that timezone names are generated correctly for fixed offsets."""
        # Positive offset with minutes
        date1 = Date.from_iso("2024-01-15T10:30:00+05:30")
        assert "UTC+05:30" in date1.timezone

        # Negative offset without minutes
        date2 = Date.from_iso("2024-01-15T10:30:00-08:00")
        assert "UTC-08" in date2.timezone

        # Zero offset
        date3 = Date.from_iso("2024-01-15T10:30:00+00:00")
        assert date3.timezone == "UTC"


# ==== COVERAGE IMPROVEMENTS TESTS ====


class TestDateCoverageImprovements:
    """Tests to cover uncovered lines in Date class."""

    def test_date_constructor_with_none_tz(self):
        """Test Date constructor when tz=None (line 36)."""
        # This should default to UTC
        date = Date(tz=None)
        assert date._zone.key == "UTC"

    def test_now_invalid_naive_value(self):
        """Test Date.now with invalid naive parameter (lines 176-179)."""
        with pytest.raises(ValueError, match="Invalid 'naive' value"):
            Date.now(naive="invalid")

    def test_from_iso_with_invalid_format_causing_value_error(self):
        """Test from_iso with format that causes ValueError (lines 345-346)."""
        from eones.errors import InvalidFormatError

        # Invalid ISO format should raise InvalidFormatError
        with pytest.raises(InvalidFormatError):
            Date.from_iso("invalid-format")

    def test_from_iso_with_invalid_timezone(self):
        """Test from_iso with invalid timezone causing ZoneInfoNotFoundError (line 351)."""
        from eones.errors import InvalidTimezoneError

        # Test with naive datetime and invalid timezone
        with pytest.raises(InvalidTimezoneError):
            Date.from_iso("2024-01-01T12:00:00", tz="Invalid/Timezone")

    def test_from_iso_with_utc_timezone(self):
        """Test from_iso with datetime having timezone.utc (line 363)."""
        from datetime import timezone
        from unittest.mock import patch

        # Create a datetime with timezone.utc
        dt_with_utc = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        # Mock fromisoformat to return this datetime
        with patch("eones.core.date.datetime") as mock_datetime:
            mock_datetime.fromisoformat.return_value = dt_with_utc
            mock_datetime.now.return_value = datetime.now()

            date = Date.from_iso("2024-01-01T12:00:00Z")
            assert date is not None

    def test_from_iso_with_offset_having_minutes(self):
        """Test from_iso with timezone offset having non-zero minutes (line 380)."""
        # Test with offset like +05:30 (India Standard Time)
        date = Date.from_iso("2024-01-01T12:00:00+05:30")
        assert date is not None
        # The timezone name should include minutes
        assert "30" in date._zone.key

    def test_from_unix_with_none_tz_explicit(self):
        """Test from_unix with tz=None explicitly to trigger line 395."""
        # This should trigger the tz = "UTC" assignment on line 395
        date = Date.from_unix(1640995200.0, tz=None)
        assert date is not None
        assert date._zone.key == "UTC"

    def test_from_unix_with_invalid_timezone(self):
        """Test from_unix with invalid timezone (line 410)."""
        from eones.errors import InvalidTimezoneError

        timestamp = 1704110400.0  # 2024-01-01 12:00:00 UTC

        with pytest.raises(InvalidTimezoneError):
            Date.from_unix(timestamp, tz="Invalid/Timezone")

    def test_from_iso_naive_datetime_with_invalid_tz_precise(self):
        """Test from_iso with naive datetime and invalid timezone (line 351)."""
        from eones.errors import InvalidTimezoneError

        # Test with ISO string without timezone info and invalid tz parameter
        # This should trigger the ZoneInfoNotFoundError and line 351
        with pytest.raises(InvalidTimezoneError):
            Date.from_iso("2024-01-01T12:00:00", tz="Invalid/Timezone/Name")

    def test_from_iso_with_fixed_offset_timezone(self):
        """Test from_iso with fixed offset timezone to trigger line 363."""
        from datetime import timedelta, timezone
        from unittest.mock import patch

        # Create a datetime with a fixed offset (not timezone.utc)
        fixed_offset = timezone(timedelta(hours=5))
        dt_with_fixed = datetime(2024, 1, 1, 12, 0, 0, tzinfo=fixed_offset)

        # Mock fromisoformat to return this datetime with fixed offset
        with patch("eones.core.date.datetime") as mock_datetime:
            mock_datetime.fromisoformat.return_value = dt_with_fixed

            date = Date.from_iso("2024-01-01T12:00:00+05:00")
            assert date is not None

    def test_from_iso_with_timezone_utc_object_direct(self):
        """Test from_iso with timezone.utc object (line 363)."""
        # Test with actual ISO string that has timezone info
        # This should parse to a datetime with timezone.utc
        date = Date.from_iso("2024-01-01T12:00:00+00:00")
        assert date is not None
        # The datetime should have timezone info and trigger line 363
        assert date._zone.key == "UTC"

    def test_from_iso_offset_with_nonzero_minutes_precise(self):
        """Test from_iso with offset having non-zero minutes (line 380)."""
        # Test with actual ISO string that has timezone offset with minutes
        # This should trigger the line 380 condition where minutes != 0
        date = Date.from_iso("2024-01-01T12:00:00+05:30")
        assert date is not None
        # Should create a timezone name with minutes
        assert ":30" in date._zone.key
        assert date._zone.key == "UTC+05:30"
