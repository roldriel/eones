"""tests/unit/test_calendars.py"""

from __future__ import annotations

import pytest

from eones.calendars import (
    HolidayCalendar,
    _make_date,
    available_calendars,
    get_calendar,
    last_weekday_of_month,
    nth_weekday_of_month,
    register_calendar,
)

# ==== Fixtures ====


@pytest.fixture
def ar_cal():
    """Argentina holiday calendar."""
    return get_calendar("America/Argentina")


@pytest.fixture
def us_cal():
    """US holiday calendar."""
    return get_calendar("America/US")


@pytest.fixture
def fr_cal():
    """France holiday calendar."""
    return get_calendar("Europe/France")


@pytest.fixture
def de_cal():
    """Germany holiday calendar."""
    return get_calendar("Europe/Germany")


@pytest.fixture
def es_cal():
    """Spain holiday calendar."""
    return get_calendar("Europe/Spain")


@pytest.fixture
def jp_cal():
    """Japan holiday calendar."""
    return get_calendar("Asia/Japan")


@pytest.fixture
def au_cal():
    """Australia holiday calendar."""
    return get_calendar("Oceania/Australia")


# ==== TestHolidayCount ====


class TestHolidayCount:
    """Verify total holiday count for each calendar for year 2026."""

    @pytest.mark.parametrize(
        "calendar_name, expected_count",
        [
            ("America/Argentina", 15),
            ("America/US", 11),
            ("Europe/France", 11),
            ("Europe/Germany", 9),
            ("Europe/Spain", 10),
            ("Asia/Japan", 16),
            ("Oceania/Australia", 9),
        ],
    )
    def test_holiday_count_2026(self, calendar_name, expected_count):
        cal = get_calendar(calendar_name)
        holidays = cal.holidays(2026)
        assert len(holidays) == expected_count


# ==== TestFixedHolidays ====


class TestFixedHolidays:
    """Verify fixed date holidays are present for each calendar."""

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (5, 25),
            (7, 9),
            (12, 25),
        ],
    )
    def test_argentina_fixed(self, ar_cal, month, day):
        holidays = ar_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (7, 4),
            (12, 25),
        ],
    )
    def test_us_fixed(self, us_cal, month, day):
        holidays = us_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (5, 1),
            (7, 14),
            (12, 25),
        ],
    )
    def test_france_fixed(self, fr_cal, month, day):
        holidays = fr_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (5, 1),
            (10, 3),
            (12, 25),
            (12, 26),
        ],
    )
    def test_germany_fixed(self, de_cal, month, day):
        holidays = de_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (1, 6),
            (5, 1),
            (12, 25),
        ],
    )
    def test_spain_fixed(self, es_cal, month, day):
        holidays = es_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (2, 11),
            (5, 3),
        ],
    )
    def test_japan_fixed(self, jp_cal, month, day):
        holidays = jp_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays

    @pytest.mark.parametrize(
        "month, day",
        [
            (1, 1),
            (1, 26),
            (4, 25),
            (12, 25),
        ],
    )
    def test_australia_fixed(self, au_cal, month, day):
        holidays = au_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays


# ==== TestMovableHolidays ====


class TestMovableHolidays:
    """Verify Easter-based and rule-based holidays for 2026.

    Easter 2026 falls on April 5.
    """

    @pytest.mark.parametrize(
        "month, day, description",
        [
            (2, 16, "Carnival Monday (Easter-48)"),
            (2, 17, "Carnival Tuesday (Easter-47)"),
            (4, 3, "Good Friday (Easter-2)"),
        ],
    )
    def test_argentina_movable(self, ar_cal, month, day, description):
        holidays = ar_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays, description

    @pytest.mark.parametrize(
        "month, day, description",
        [
            (1, 19, "MLK Day (3rd Mon Jan)"),
            (5, 25, "Memorial Day (last Mon May)"),
            (11, 26, "Thanksgiving (4th Thu Nov)"),
        ],
    )
    def test_us_movable(self, us_cal, month, day, description):
        holidays = us_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays, description

    @pytest.mark.parametrize(
        "month, day, description",
        [
            (4, 6, "Easter Monday"),
            (5, 14, "Ascension (Easter+39)"),
            (5, 25, "Whit Monday (Easter+50)"),
        ],
    )
    def test_france_movable(self, fr_cal, month, day, description):
        holidays = fr_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays, description

    @pytest.mark.parametrize(
        "month, day, description",
        [
            (4, 3, "Good Friday (Easter-2)"),
            (4, 6, "Easter Monday"),
            (5, 14, "Ascension (Easter+39)"),
            (5, 25, "Whit Monday (Easter+50)"),
        ],
    )
    def test_germany_movable(self, de_cal, month, day, description):
        holidays = de_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays, description

    def test_spain_good_friday(self, es_cal):
        holidays = es_cal.holidays(2026)
        good_friday = _make_date(2026, 4, 3)
        assert good_friday in holidays

    @pytest.mark.parametrize(
        "month, day, description",
        [
            (1, 12, "Coming of Age Day (2nd Mon Jan)"),
            (7, 20, "Marine Day (3rd Mon Jul)"),
            (9, 21, "Respect for Aged Day (3rd Mon Sep)"),
            (10, 12, "Sports Day (2nd Mon Oct)"),
        ],
    )
    def test_japan_movable(self, jp_cal, month, day, description):
        holidays = jp_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays, description

    @pytest.mark.parametrize(
        "month, day, description",
        [
            (4, 3, "Good Friday (Easter-2)"),
            (4, 4, "Easter Saturday (Easter-1)"),
            (4, 6, "Easter Monday (Easter+1)"),
            (6, 8, "Queen's Birthday (2nd Mon Jun)"),
        ],
    )
    def test_australia_movable(self, au_cal, month, day, description):
        holidays = au_cal.holidays(2026)
        expected = _make_date(2026, month, day)
        assert expected in holidays, description


# ==== TestIsHoliday ====


class TestIsHoliday:
    """Verify is_holiday returns correct boolean values."""

    def test_is_holiday_true_argentina(self, ar_cal):
        date = _make_date(2026, 1, 1)
        assert ar_cal.is_holiday(date) is True

    def test_is_holiday_false_argentina(self, ar_cal):
        date = _make_date(2026, 3, 15)
        assert ar_cal.is_holiday(date) is False

    def test_is_holiday_true_us(self, us_cal):
        date = _make_date(2026, 7, 4)
        assert us_cal.is_holiday(date) is True

    def test_is_holiday_false_us(self, us_cal):
        date = _make_date(2026, 7, 5)
        assert us_cal.is_holiday(date) is False

    def test_is_holiday_true_france(self, fr_cal):
        date = _make_date(2026, 7, 14)
        assert fr_cal.is_holiday(date) is True

    def test_is_holiday_false_germany(self, de_cal):
        date = _make_date(2026, 6, 15)
        assert de_cal.is_holiday(date) is False

    def test_is_holiday_true_spain(self, es_cal):
        date = _make_date(2026, 12, 25)
        assert es_cal.is_holiday(date) is True

    def test_is_holiday_true_japan(self, jp_cal):
        date = _make_date(2026, 1, 1)
        assert jp_cal.is_holiday(date) is True

    def test_is_holiday_true_australia(self, au_cal):
        date = _make_date(2026, 1, 26)
        assert au_cal.is_holiday(date) is True


# ==== TestHolidayName ====


class TestHolidayName:
    """Verify holiday_name returns correct names or None."""

    def test_argentina_new_year(self, ar_cal):
        date = _make_date(2026, 1, 1)
        assert ar_cal.holiday_name(date) == "Año Nuevo"

    def test_argentina_carnival_monday(self, ar_cal):
        date = _make_date(2026, 2, 16)
        assert ar_cal.holiday_name(date) == "Carnaval (Lunes)"

    def test_argentina_non_holiday(self, ar_cal):
        date = _make_date(2026, 3, 15)
        assert ar_cal.holiday_name(date) is None

    def test_us_independence_day(self, us_cal):
        date = _make_date(2026, 7, 4)
        assert us_cal.holiday_name(date) == "Independence Day"

    def test_us_thanksgiving(self, us_cal):
        date = _make_date(2026, 11, 26)
        assert us_cal.holiday_name(date) == "Thanksgiving Day"

    def test_us_non_holiday(self, us_cal):
        date = _make_date(2026, 8, 1)
        assert us_cal.holiday_name(date) is None

    def test_france_bastille_day(self, fr_cal):
        date = _make_date(2026, 7, 14)
        assert fr_cal.holiday_name(date) == "Fête Nationale"

    def test_france_easter_monday(self, fr_cal):
        date = _make_date(2026, 4, 6)
        assert fr_cal.holiday_name(date) == "Lundi de Pâques"

    def test_france_non_holiday(self, fr_cal):
        date = _make_date(2026, 6, 15)
        assert fr_cal.holiday_name(date) is None

    def test_germany_christmas_first(self, de_cal):
        date = _make_date(2026, 12, 25)
        assert de_cal.holiday_name(date) == "1. Weihnachtstag"

    def test_germany_christmas_second(self, de_cal):
        date = _make_date(2026, 12, 26)
        assert de_cal.holiday_name(date) == "2. Weihnachtstag"

    def test_germany_non_holiday(self, de_cal):
        date = _make_date(2026, 7, 1)
        assert de_cal.holiday_name(date) is None

    def test_spain_epiphany(self, es_cal):
        date = _make_date(2026, 1, 6)
        assert es_cal.holiday_name(date) == "Epifanía del Señor"

    def test_spain_good_friday(self, es_cal):
        date = _make_date(2026, 4, 3)
        assert es_cal.holiday_name(date) == "Viernes Santo"

    def test_spain_non_holiday(self, es_cal):
        date = _make_date(2026, 3, 15)
        assert es_cal.holiday_name(date) is None

    def test_japan_new_year(self, jp_cal):
        date = _make_date(2026, 1, 1)
        assert jp_cal.holiday_name(date) == "元日"

    def test_japan_coming_of_age(self, jp_cal):
        date = _make_date(2026, 1, 12)
        assert jp_cal.holiday_name(date) == "成人の日"

    def test_japan_non_holiday(self, jp_cal):
        date = _make_date(2026, 6, 15)
        assert jp_cal.holiday_name(date) is None

    def test_australia_australia_day(self, au_cal):
        date = _make_date(2026, 1, 26)
        assert au_cal.holiday_name(date) == "Australia Day"

    def test_australia_good_friday(self, au_cal):
        date = _make_date(2026, 4, 3)
        assert au_cal.holiday_name(date) == "Good Friday"

    def test_australia_queens_birthday(self, au_cal):
        date = _make_date(2026, 6, 8)
        assert au_cal.holiday_name(date) == "Queen's Birthday"

    def test_australia_non_holiday(self, au_cal):
        date = _make_date(2026, 7, 1)
        assert au_cal.holiday_name(date) is None


# ==== TestHelpers ====


class TestHelpers:
    """Test nth_weekday_of_month and last_weekday_of_month helpers."""

    @pytest.mark.parametrize(
        "year, month, weekday, n, expected_day",
        [
            (2026, 1, 0, 1, 5),  # 1st Monday Jan 2026 = Jan 5
            (2026, 1, 0, 3, 19),  # 3rd Monday Jan 2026 = Jan 19
            (2026, 6, 0, 2, 8),  # 2nd Monday Jun 2026 = Jun 8
        ],
    )
    def test_nth_weekday_of_month(self, year, month, weekday, n, expected_day):
        result = nth_weekday_of_month(year, month, weekday, n)
        dt = result.to_datetime()
        assert dt.day == expected_day
        assert dt.weekday() == weekday

    def test_nth_weekday_of_month_raises_on_impossible(self):
        with pytest.raises(ValueError):
            nth_weekday_of_month(2026, 2, 0, 5)

    def test_last_weekday_of_month(self):
        result = last_weekday_of_month(2026, 5, 0)
        dt = result.to_datetime()
        assert dt.day == 25
        assert dt.month == 5
        assert dt.weekday() == 0

    def test_last_weekday_of_december(self):
        result = last_weekday_of_month(2026, 12, 0)
        dt = result.to_datetime()
        assert dt.day == 28
        assert dt.month == 12
        assert dt.weekday() == 0


# ==== TestRegistry ====


class TestRegistry:
    """Test calendar registry functions."""

    def test_get_calendar_returns_instance(self):
        cal = get_calendar("America/Argentina")
        assert isinstance(cal, HolidayCalendar)

    def test_get_calendar_raises_for_unknown(self):
        with pytest.raises(ValueError, match="Unknown calendar"):
            get_calendar("Unknown/Calendar")

    def test_available_calendars_returns_sorted_list(self):
        calendars = available_calendars()
        assert isinstance(calendars, list)
        assert calendars == sorted(calendars)
        expected = [
            "America/Argentina",
            "America/US",
            "Asia/Japan",
            "Europe/France",
            "Europe/Germany",
            "Europe/Spain",
            "Oceania/Australia",
        ]
        for name in expected:
            assert name in calendars

    def test_register_and_get_custom_calendar(self):
        class _TestCalendar(HolidayCalendar):
            def holidays(self, year):
                return [_make_date(year, 6, 15)]

            def holiday_name(self, date):
                if date.month == 6 and date.day == 15:
                    return "Test Day"
                return None

        register_calendar("Custom/Test", _TestCalendar)
        cal = get_calendar("Custom/Test")
        assert isinstance(cal, HolidayCalendar)
        holidays = cal.holidays(2026)
        assert len(holidays) == 1
        assert cal.is_holiday(_make_date(2026, 6, 15)) is True
        assert cal.holiday_name(_make_date(2026, 6, 15)) == "Test Day"
        assert cal.holiday_name(_make_date(2026, 6, 16)) is None

    def test_custom_calendar_in_available_calendars(self):
        assert "Custom/Test" in available_calendars()


class TestArgentinaHolidayNames:
    """Cover all holiday_name branches in argentina.py."""

    @pytest.mark.parametrize(
        "month, day, expected_name",
        [
            (1, 1, "Año Nuevo"),
            (3, 24, "Día Nacional de la Memoria"),
            (4, 2, "Veterano"),
            (5, 1, "Trabajo"),
            (5, 25, "Revolución de Mayo"),
            (6, 17, "Güemes"),
            (7, 9, "Independencia"),
            (12, 8, "Inmaculada Concepción"),
            (12, 25, "Navidad"),
        ],
    )
    def test_fixed_holiday_names(self, month, day, expected_name):
        cal = get_calendar("America/Argentina")
        d = _make_date(2026, month, day)
        name = cal.holiday_name(d)
        assert name is not None
        assert expected_name in name

    def test_carnival_monday_name(self):
        """Carnival Monday 2026 = Feb 16 (Easter Apr 5 - 48)."""
        cal = get_calendar("America/Argentina")
        d = _make_date(2026, 2, 16)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Carnaval" in name

    def test_carnival_tuesday_name(self):
        """Carnival Tuesday 2026 = Feb 17 (Easter Apr 5 - 47)."""
        cal = get_calendar("America/Argentina")
        d = _make_date(2026, 2, 17)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Carnaval" in name

    def test_good_friday_name(self):
        """Good Friday 2026 = Apr 3 (Easter Apr 5 - 2)."""
        cal = get_calendar("America/Argentina")
        d = _make_date(2026, 4, 3)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Viernes Santo" in name

    def test_san_martin_name(self):
        """3rd Monday August 2026 = Aug 17."""
        cal = get_calendar("America/Argentina")
        from eones.calendars import nth_weekday_of_month

        d = nth_weekday_of_month(2026, 8, 0, 3)
        name = cal.holiday_name(d)
        assert name is not None
        assert "San Martín" in name

    def test_diversidad_cultural_name(self):
        """2nd Monday October 2026 = Oct 12."""
        cal = get_calendar("America/Argentina")
        from eones.calendars import nth_weekday_of_month

        d = nth_weekday_of_month(2026, 10, 0, 2)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Diversidad" in name

    def test_soberania_name(self):
        """4th Monday November 2026 = Nov 23."""
        cal = get_calendar("America/Argentina")
        from eones.calendars import nth_weekday_of_month

        d = nth_weekday_of_month(2026, 11, 0, 4)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Soberanía" in name

    def test_non_holiday_returns_none(self):
        cal = get_calendar("America/Argentina")
        d = _make_date(2026, 3, 15)
        assert cal.holiday_name(d) is None


class TestFranceHolidayNames:
    """Cover all holiday_name branches in france.py."""

    def test_easter_monday_name(self):
        """Easter Monday 2026 = Apr 6."""
        cal = get_calendar("Europe/France")
        d = _make_date(2026, 4, 6)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Pâques" in name

    def test_ascension_name(self):
        """Ascension 2026 = May 14 (Easter + 39)."""
        cal = get_calendar("Europe/France")
        d = _make_date(2026, 5, 14)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Ascension" in name

    def test_whit_monday_name(self):
        """Whit Monday 2026 = May 25 (Easter + 50)."""
        cal = get_calendar("Europe/France")
        d = _make_date(2026, 5, 25)
        name = cal.holiday_name(d)
        assert name is not None
        assert "Pentecôte" in name


class TestJapanHolidayNames:
    """Cover holiday_name branches in japan.py."""

    def test_vernal_equinox_name(self):
        """Vernal equinox around March 20-21."""
        cal = get_calendar("Asia/Japan")
        # Try March 20 and 21 for 2026
        for day in (20, 21):
            d = _make_date(2026, 3, day)
            name = cal.holiday_name(d)
            if name is not None:
                assert "春分" in name
                break
        else:
            pytest.fail("Vernal equinox not found on Mar 20 or 21")

    def test_autumnal_equinox_name(self):
        """Autumnal equinox around Sep 22-23."""
        cal = get_calendar("Asia/Japan")
        for day in (22, 23):
            d = _make_date(2026, 9, day)
            name = cal.holiday_name(d)
            if name is not None:
                assert "秋分" in name
                break
        else:
            pytest.fail("Autumnal equinox not found on Sep 22 or 23")

    def test_substitute_holiday(self):
        """Test substitute holiday (振替休日) when holiday falls on Sunday.

        Find a year where a fixed holiday falls on Sunday.
        Feb 11 2024 is Sunday -> Feb 12 should be substitute.
        """
        cal = get_calendar("Asia/Japan")
        d = _make_date(2024, 2, 12)
        name = cal.holiday_name(d)
        assert name is not None
        assert "振替休日" in name

    def test_movable_holiday_name(self):
        """Coming of Age Day: 2nd Monday Jan 2026 = Jan 12."""
        cal = get_calendar("Asia/Japan")
        d = _make_date(2026, 1, 12)
        name = cal.holiday_name(d)
        assert name is not None
        assert "成人" in name
