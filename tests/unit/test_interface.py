"""tests/unit/test_interface.py"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from eones.core.date import Date
from eones.core.delta import Delta
from eones.errors import InvalidFormatError
from eones.interface import Eones

# ==== INIT ====


@pytest.mark.parametrize(
    "formats, additional_formats",
    [
        (["%Y-%m-%d"], ["%d-%m-%Y"]),
        ("%Y-%m-%d", ["%d-%m-%Y"]),
        (["%Y-%m-%d"], "%d-%m-%Y"),
        ("%Y-%m-%d", "%d-%m-%Y"),
    ],
)
def test_eones_init_mutual_exclusion_raises(formats, additional_formats):
    with pytest.raises(
        ValueError, match="Use either 'formats' or 'additional_formats'"
    ):
        Eones("2024-01-01", formats=formats, additional_formats=additional_formats)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"formats": "%Y-%m-%d"},
        {"additional_formats": "%Y-%m-%d"},
        {"additional_formats": ["%Y-%m-%d"]},
    ],
)
def test_eones_init_format_variants(kwargs):
    e = Eones("2024-01-01", **kwargs)
    assert isinstance(e, Eones)


# ==== REPRESENTATION & COMPARISON ====


def test_eones_repr_contains_date_and_tz():
    e = Eones("2025-06-15T14:30:00", tz="UTC")
    representation = repr(e)
    assert "Eones(date=" in representation
    assert "tz='UTC'" in representation


def test_eones_equality_same_value():
    a = Eones("2024-01-01", tz="UTC")
    b = Eones("2024-01-01", tz="UTC")
    assert a == b


def test_eones_equality_not_instance():
    a = Eones("2024-01-01", tz="UTC")
    assert a != "2024-01-01"


def test_ergonomic_add_subtract():
    e = Eones("2023-01-01")
    delta = Delta(days=2)

    # Positional Delta
    e.add(delta)
    assert e.now().day == 3

    # Positional timedelta
    e.add(timedelta(days=1))
    assert e.now().day == 4

    # Keyword arguments
    e.add(days=1)
    assert e.now().day == 5

    # Subtract positional
    e.subtract(delta)
    assert e.now().day == 3


def test_range_iter():
    start = Date(datetime(2023, 1, 1), naive="utc")
    end = Date(datetime(2023, 1, 5), naive="utc")
    step = timedelta(days=1)

    dates = list(Eones.range_iter(start, end, step))
    assert len(dates) == 5
    assert dates[0].day == 1
    assert dates[-1].day == 5


def test_easter_date():
    # Easter 2024 is March 31
    ed = Eones.easter_date(2024)
    assert ed.month == 3
    assert ed.day == 31

    # Easter 2025 is April 20
    ed2 = Eones.easter_date(2025)
    assert ed2.month == 4
    assert ed2.day == 20


# ==== TIME TRANSFORMATIONS ====


@pytest.mark.parametrize(
    "method, unit",
    [
        ("floor", "hour"),
        ("ceil", "hour"),
        ("round", "day"),
        ("start_of", "month"),
        ("end_of", "month"),
    ],
)
def test_eones_unit_transformations(method, unit):
    e = Eones("2024-03-17T15:45:23")
    transformed = getattr(e, method)(unit)
    assert isinstance(transformed, Eones)


def test_replace_method_changes_date_fields():
    e = Eones("2024-01-15", tz="UTC")
    result = e.replace(month=12, day=25)
    assert isinstance(result, Eones)
    dt = result.now().to_datetime()
    assert dt.month == 12
    assert dt.day == 25


def test_next_weekday_returns_correct_type():
    e = Eones("2025-01-01", tz="UTC")
    result = e.next_weekday(4)
    assert isinstance(result, Date)


# ==== RANGE & POSITIONAL CHECKS ====


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


@pytest.mark.parametrize(
    "compare, expected, check_month",
    [
        ("2025-06-01", True, True),
        ({"year": 2025, "month": 6, "day": 1}, True, True),
        (datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC")), True, True),
        (Date(datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC"))), True, True),
        (Date(datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))), True, False),
    ],
)
def test_is_within_variants(compare, expected, check_month):
    z = Eones("2025-06-15", tz="UTC")
    assert z.is_within(compare, check_month=check_month) is expected


def test_is_between_inclusive_true():
    e = Eones("2025-01-15", tz="UTC")
    assert e.is_between("2025-01-01", "2025-01-31", inclusive=True) is True


def test_is_between_inclusive_false_outside():
    e = Eones("2025-01-01", tz="UTC")
    assert e.is_between("2025-01-01", "2025-01-15", inclusive=False) is False


def test_is_same_week_with_eones_instance():
    e1 = Eones("2024-01-01")
    e2 = Eones("2024-01-02")
    assert e1.is_same_week(e2) is True


def test_is_same_week_with_datetime_input():
    dt = datetime(2025, 1, 2, tzinfo=ZoneInfo("UTC"))
    e = Eones("2025-01-01", tz="UTC")
    assert e.is_same_week(dt) is True


# ==== DIFFERENCE ====


@pytest.mark.parametrize(
    "a,b,unit,expected",
    [
        ("2024-01-01", "2024-01-03", "days", 2),
        ("2024-01-01", "2024-01-15", "weeks", 2),
        ("2024-01-01", "2024-04-01", "months", 3),
        ("2022-01-01", "2024-01-01", "years", 2),
    ],
)
def test_difference_units(a, b, unit, expected):
    z = Eones(a)
    result = z.difference(b, unit=unit)
    assert result == expected


def test_difference_with_eones_instance():
    a = Eones("2025-01-01", tz="UTC")
    b = Eones("2025-01-15", tz="UTC")
    assert a.difference(b, unit="days") == 14


def test_difference_with_date_instance():
    dt = datetime(2025, 1, 15, tzinfo=ZoneInfo("UTC"))
    d = Date(dt)
    e = Eones("2025-01-01", tz="UTC")
    assert e.difference(d, unit="days") == 14


def test_coerce_to_date_from_eones():
    a = Eones("2024-01-01", tz="UTC")
    b = Eones("2024-01-15", tz="UTC")
    coerced = a._coerce_to_date(b)
    assert isinstance(coerced, Date)
    assert coerced.to_datetime().day == 15


def test_diff_for_humans_english_and_spanish():
    start = Eones("2025-01-10", tz="UTC")
    end = Eones("2025-01-17", tz="UTC")

    assert start.diff_for_humans(end, locale="en") == "1 week ago"
    assert end.diff_for_humans(start, locale="en") == "in 1 week"

    assert start.diff_for_humans(end, locale="es") == "hace 1 semana"
    assert end.diff_for_humans(start, locale="es") == "en 1 semana"


def test_diff_for_humans_french_and_german():
    start = Eones("2025-01-10", tz="UTC")
    end = Eones("2025-01-17", tz="UTC")

    assert start.diff_for_humans(end, locale="fr") == "il y a 1 semaine"
    assert end.diff_for_humans(start, locale="fr") == "dans 1 semaine"

    assert start.diff_for_humans(end, locale="de") == "vor 1 Woche"
    assert end.diff_for_humans(start, locale="de") == "in 1 Woche"


# ==== PARSING COHERENCE ====


@pytest.mark.parametrize(
    "value",
    [
        "2024-01-15",
        "2024-01-15T10:30:00",
        "2024-01-15T10:30:00Z",
        "15/01/2024",
        "2024-01-15 13:45:00",
        {"year": 2024, "month": 1, "day": 15},
        datetime(2024, 1, 15, 10, 30, tzinfo=ZoneInfo("UTC")),
    ],
)
def test_parsing_coherence_between_entrypoints(value):
    """Verify that Eones and parse_date (utility) yield identical results."""
    from eones import parse_date

    e1 = Eones(value)
    e2 = parse_date(value)

    assert e1.now() == e2
    assert e1.now().to_datetime() == e2.to_datetime()
    assert e1.now().timezone == e2.timezone


def test_parsing_error_coherence():
    """Verify that both entrypoints raise the same errors for bad inputs."""
    from eones import parse_date

    bad_value = "invalid format string"
    with pytest.raises(InvalidFormatError):
        Eones(bad_value)
    with pytest.raises(InvalidFormatError):
        parse_date(bad_value)

    bad_logical_value = "2024-02-30"  # Invalid day
    with pytest.raises(ValueError, match="day.*(out of range|must be in range)"):
        Eones(bad_logical_value)
    with pytest.raises(ValueError, match="day.*(out of range|must be in range)"):
        parse_date(bad_logical_value)


def test_parsing_coherence_with_custom_tz():
    """Verify coherence when using a custom timezone."""
    from eones import parse_date

    tz = "America/New_York"
    value = "2024-01-15 10:30:00"

    e1 = Eones(value, tz=tz)
    # Note: parse_date also uses DEFAULT_FORMATS and should support this
    e2 = parse_date(value, tz=tz)

    assert e1.now() == e2
    assert e1.now().timezone == tz
    assert e2.timezone == tz


# ==== CONSTRUCTOR DEFAULTS (locale, calendar) ====


class TestConstructorDefaults:
    """Test locale and calendar constructor defaults (Option C)."""

    def test_default_locale_is_english(self):
        e = Eones("2026-01-01")
        assert e._locale == "en"

    def test_default_calendar_is_none(self):
        e = Eones("2026-01-01")
        assert e._calendar is None

    def test_custom_locale(self):
        e = Eones("2026-01-01", locale="es")
        assert e._locale == "es"

    def test_custom_calendar(self):
        e = Eones("2026-01-01", calendar="America/Argentina")
        assert e._calendar == "America/Argentina"

    def test_copy_preserves_locale_and_calendar(self):
        e = Eones("2026-01-01", locale="ja", calendar="Asia/Japan")
        c = e.copy()
        assert c._locale == "ja"
        assert c._calendar == "Asia/Japan"

    def test_clone_preserves_locale_and_calendar(self):
        e = Eones("2026-01-01", locale="de", calendar="Europe/Germany")
        c = e.clone()
        assert c._locale == "de"
        assert c._calendar == "Europe/Germany"

    def test_eones_to_eones_copies_locale_calendar(self):
        e1 = Eones("2026-01-01", locale="fr", calendar="Europe/France")
        e2 = Eones(e1)
        assert e2._locale == "fr"
        assert e2._calendar == "Europe/France"


# ==== DIFF FOR HUMANS WITH INSTANCE LOCALE ====


class TestDiffForHumansInstanceLocale:

    def test_inherits_locale_from_constructor(self):
        e = Eones("2026-01-10", locale="es")
        result = e.diff_for_humans("2026-01-17")
        assert "semana" in result

    def test_override_locale(self):
        e = Eones("2026-01-10", locale="es")
        result = e.diff_for_humans("2026-01-17", locale="en")
        assert "week" in result

    def test_japanese_locale(self):
        e = Eones("2026-01-10", locale="ja")
        result = e.diff_for_humans("2026-01-17")
        assert "\u9031\u9593" in result


# ==== FORMAT LOCALE ====


class TestFormatLocale:

    def test_spanish_full_date(self):
        e = Eones("2026-05-25", locale="es")
        result = e.format_locale("DD de MMMM de YYYY")
        assert result == "25 de mayo de 2026"

    def test_english_full_date(self):
        e = Eones("2026-05-25", locale="en")
        result = e.format_locale("MMMM DD, YYYY")
        assert result == "May 25, 2026"

    def test_japanese_format(self):
        e = Eones("2026-03-15", locale="ja")
        assert "3\u6708" in e.format_locale("YYYY\u5e74MM\u6708DD\u65e5")

    def test_override_locale(self):
        e = Eones("2026-05-25", locale="es")
        result = e.format_locale("MMMM DD", locale="en")
        assert result == "May 25"

    def test_day_name_token(self):
        e = Eones("2026-05-25", locale="es")  # Monday
        result = e.format_locale("dddd DD")
        assert "lunes" in result


# ==== HOLIDAY METHODS ====


class TestEonesIsHoliday:

    def test_holiday_with_calendar(self):
        e = Eones("2026-05-25", calendar="America/Argentina")
        assert e.is_holiday() is True

    def test_non_holiday(self):
        e = Eones("2026-05-26", calendar="America/Argentina")
        assert e.is_holiday() is False

    def test_no_calendar_returns_false(self):
        e = Eones("2026-05-25")
        assert e.is_holiday() is False

    def test_override_calendar(self):
        e = Eones("2026-07-14", calendar="America/Argentina")
        # Jul 14 is not AR holiday but is France holiday
        assert e.is_holiday() is False
        assert e.is_holiday(calendar="Europe/France") is True


class TestEonesHolidayName:

    def test_returns_name(self):
        e = Eones("2026-05-25", calendar="America/Argentina")
        name = e.holiday_name()
        assert name is not None
        assert "Mayo" in name or "Revoluci\u00f3n" in name or "mayo" in name

    def test_non_holiday_returns_none(self):
        e = Eones("2026-05-26", calendar="America/Argentina")
        assert e.holiday_name() is None

    def test_no_calendar_returns_none(self):
        e = Eones("2026-05-25")
        assert e.holiday_name() is None


# ==== BUSINESS DAY METHODS ====


class TestEonesBusinessDay:

    def test_is_business_day_weekday(self):
        e = Eones("2026-01-05")  # Monday
        assert e.is_business_day() is True

    def test_is_business_day_weekend(self):
        e = Eones("2026-01-10")  # Saturday
        assert e.is_business_day() is False

    def test_is_business_day_holiday(self):
        e = Eones("2026-01-01", calendar="America/Argentina")
        assert e.is_business_day() is False

    def test_next_business_day(self):
        e = Eones("2026-01-09")  # Friday
        result = e.next_business_day()
        assert isinstance(result, Eones)
        assert result.to_datetime().day == 12  # Monday

    def test_previous_business_day(self):
        e = Eones("2026-01-12")  # Monday
        result = e.previous_business_day()
        assert isinstance(result, Eones)
        assert result.to_datetime().day == 9  # Friday

    def test_add_business_days(self):
        e = Eones("2026-01-05")  # Monday
        result = e.add_business_days(5)
        assert isinstance(result, Eones)
        assert result.to_datetime().day == 12  # Next Monday

    def test_subtract_business_days(self):
        e = Eones("2026-01-12")  # Monday
        result = e.subtract_business_days(5)
        assert isinstance(result, Eones)
        assert result.to_datetime().day == 5  # Previous Monday

    def test_time_until_weekend(self):
        e = Eones("2026-01-05")  # Monday
        assert e.time_until_weekend() == 5

    def test_time_until_business_day_on_weekend(self):
        e = Eones("2026-01-10")  # Saturday
        assert e.time_until_business_day() == 2

    def test_time_until_business_day_on_weekday(self):
        e = Eones("2026-01-05")  # Monday
        assert e.time_until_business_day() == 0

    def test_business_day_with_calendar_resolution(self):
        e = Eones("2026-01-01", calendar="America/Argentina")
        # Jan 1 is holiday, next business day should skip it
        e.next_business_day()
        assert e.to_datetime().day == 2  # Jan 2 Friday


# ==== STATIC BUSINESS METHODS ====


class TestEonesStaticBusinessMethods:

    def test_count_business_days(self):
        result = Eones.count_business_days("2026-01-05", "2026-01-12")
        assert result == 5

    def test_count_weekends(self):
        result = Eones.count_weekends("2026-01-05", "2026-01-12")
        assert result == 2

    def test_count_holidays(self):
        result = Eones.count_holidays(
            "2026-01-01", "2026-01-31", calendar="America/Argentina"
        )
        assert result == 1  # Jan 1 only

    def test_count_holidays_no_calendar(self):
        result = Eones.count_holidays("2026-01-01", "2026-01-31")
        assert result == 0

    def test_available_calendars(self):
        cals = Eones.available_calendars()
        assert len(cals) >= 7
        assert "America/Argentina" in cals
        assert "Asia/Japan" in cals
        assert cals == sorted(cals)
