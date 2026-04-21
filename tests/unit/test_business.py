"""tests/unit/test_business.py"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones.core.business import (
    add_business_days,
    count_business_days,
    count_holidays,
    count_weekends,
    is_business_day,
    next_business_day,
    previous_business_day,
    subtract_business_days,
    time_until_business_day,
    time_until_weekend,
)
from eones.core.date import Date


def _d(year: int, month: int, day: int) -> Date:
    """Create a UTC Date from year/month/day components."""
    return Date(datetime(year, month, day, tzinfo=ZoneInfo("UTC")), naive="utc")


# ---- Fixtures ----


@pytest.fixture
def monday():
    """Monday Jan 5 2026."""
    return _d(2026, 1, 5)


@pytest.fixture
def friday():
    """Friday Jan 9 2026."""
    return _d(2026, 1, 9)


@pytest.fixture
def saturday():
    """Saturday Jan 10 2026."""
    return _d(2026, 1, 10)


@pytest.fixture
def sunday():
    """Sunday Jan 11 2026."""
    return _d(2026, 1, 11)


@pytest.fixture
def next_monday():
    """Monday Jan 12 2026."""
    return _d(2026, 1, 12)


# ==============================================================
# is_business_day
# ==============================================================


class TestIsBusinessDay:
    """Tests for is_business_day."""

    @pytest.mark.parametrize(
        "day, expected",
        [
            (5, True),  # Monday
            (6, True),  # Tuesday
            (7, True),  # Wednesday
            (8, True),  # Thursday
            (9, True),  # Friday
            (10, False),  # Saturday
            (11, False),  # Sunday
        ],
        ids=["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
    )
    def test_weekday_detection(self, day: int, expected: bool) -> None:
        """Mon-Fri are business days, Sat-Sun are not."""
        date = _d(2026, 1, day)
        assert is_business_day(date) is expected

    def test_holiday_is_not_business_day(self) -> None:
        """Jan 1 2026 (Thu) is a holiday in America/Argentina."""
        jan1 = _d(2026, 1, 1)
        assert is_business_day(jan1, calendar="America/Argentina") is False

    def test_holiday_without_calendar_is_business_day(self) -> None:
        """Jan 1 2026 (Thu) is a regular business day without a calendar."""
        jan1 = _d(2026, 1, 1)
        assert is_business_day(jan1) is True

    def test_custom_weekend(self) -> None:
        """Friday and Saturday as weekend with custom weekend set."""
        custom_weekend = frozenset({4, 5})  # Fri=4, Sat=5
        friday = _d(2026, 1, 9)  # Friday
        saturday = _d(2026, 1, 10)  # Saturday
        sunday = _d(2026, 1, 11)  # Sunday

        assert is_business_day(friday, weekend=custom_weekend) is False
        assert is_business_day(saturday, weekend=custom_weekend) is False
        assert is_business_day(sunday, weekend=custom_weekend) is True


# ==============================================================
# next_business_day
# ==============================================================


class TestNextBusinessDay:
    """Tests for next_business_day."""

    def test_from_friday_to_monday(self, friday: Date, next_monday: Date) -> None:
        """Next business day after Friday is Monday."""
        result = next_business_day(friday)
        assert result == next_monday

    def test_from_saturday_to_monday(self, saturday: Date, next_monday: Date) -> None:
        """Next business day after Saturday is Monday."""
        result = next_business_day(saturday)
        assert result == next_monday

    def test_from_monday_to_tuesday(self, monday: Date) -> None:
        """Next business day after Monday is Tuesday."""
        result = next_business_day(monday)
        assert result == _d(2026, 1, 6)

    def test_skips_holiday(self) -> None:
        """Dec 31 2025 (Wed) -> Jan 2 2026 (Fri), skipping Jan 1 holiday."""
        dec31 = _d(2025, 12, 31)
        result = next_business_day(dec31, calendar="America/Argentina")
        assert result == _d(2026, 1, 2)


# ==============================================================
# previous_business_day
# ==============================================================


class TestPreviousBusinessDay:
    """Tests for previous_business_day."""

    def test_from_monday_to_friday(self, next_monday: Date, friday: Date) -> None:
        """Previous business day before Monday is Friday."""
        result = previous_business_day(next_monday)
        assert result == friday

    def test_from_sunday_to_friday(self, sunday: Date, friday: Date) -> None:
        """Previous business day before Sunday is Friday."""
        result = previous_business_day(sunday)
        assert result == friday

    def test_from_tuesday_to_monday(self, monday: Date) -> None:
        """Previous business day before Tuesday is Monday."""
        tuesday = _d(2026, 1, 6)
        result = previous_business_day(tuesday)
        assert result == monday

    def test_skips_holiday(self) -> None:
        """Jan 2 2026 (Fri) -> Dec 31 2025 (Wed), skipping Jan 1 holiday."""
        jan2 = _d(2026, 1, 2)
        result = previous_business_day(jan2, calendar="America/Argentina")
        assert result == _d(2025, 12, 31)


# ==============================================================
# add_business_days
# ==============================================================


class TestAddBusinessDays:
    """Tests for add_business_days."""

    def test_add_one(self, monday: Date) -> None:
        """Add 1 business day from Monday = Tuesday."""
        result = add_business_days(monday, 1)
        assert result == _d(2026, 1, 6)

    def test_add_five_crosses_weekend(self, monday: Date) -> None:
        """Add 5 business days from Monday = next Monday."""
        result = add_business_days(monday, 5)
        assert result == _d(2026, 1, 12)

    def test_add_zero_returns_same_day(self, monday: Date) -> None:
        """Add 0 business days returns the same date."""
        result = add_business_days(monday, 0)
        assert result == monday

    def test_negative_days_delegates_to_subtract(self, friday: Date) -> None:
        """Negative days delegates to subtract_business_days."""
        result = add_business_days(friday, -1)
        assert result == _d(2026, 1, 8)

    def test_add_with_calendar(self) -> None:
        """Add 1 business day from Dec 31 2025 skips Jan 1 holiday."""
        dec31 = _d(2025, 12, 31)
        result = add_business_days(dec31, 1, calendar="America/Argentina")
        assert result == _d(2026, 1, 2)


# ==============================================================
# subtract_business_days
# ==============================================================


class TestSubtractBusinessDays:
    """Tests for subtract_business_days."""

    def test_subtract_one(self) -> None:
        """Subtract 1 business day from Tuesday = Monday."""
        tuesday = _d(2026, 1, 6)
        result = subtract_business_days(tuesday, 1)
        assert result == _d(2026, 1, 5)

    def test_subtract_five_crosses_weekend(self, friday: Date) -> None:
        """Subtract 5 business days from Fri Jan 9 = Fri Jan 2."""
        result = subtract_business_days(friday, 5)
        assert result == _d(2026, 1, 2)

    def test_subtract_zero_returns_same_day(self, monday: Date) -> None:
        """Subtract 0 business days returns the same date."""
        result = subtract_business_days(monday, 0)
        assert result == monday

    def test_subtract_with_calendar(self) -> None:
        """Subtract 1 from Jan 2 2026 skips Jan 1 holiday in Argentina."""
        jan2 = _d(2026, 1, 2)
        result = subtract_business_days(jan2, 1, calendar="America/Argentina")
        assert result == _d(2025, 12, 31)


# ==============================================================
# count_business_days
# ==============================================================


class TestCountBusinessDays:
    """Tests for count_business_days."""

    def test_monday_to_friday(self, monday: Date, friday: Date) -> None:
        """Mon to Fri same week = 4 business days (exclusive of end)."""
        assert count_business_days(monday, friday) == 4

    def test_monday_to_next_monday(self, monday: Date, next_monday: Date) -> None:
        """Mon to next Mon = 5 business days."""
        assert count_business_days(monday, next_monday) == 5

    def test_same_date_returns_zero(self, monday: Date) -> None:
        """Same start and end date = 0."""
        assert count_business_days(monday, monday) == 0

    def test_with_calendar(self) -> None:
        """Jan 1-3 2026 AR: Jan 1 (holiday), Jan 2 (Fri, bday) = 1."""
        start = _d(2026, 1, 1)
        end = _d(2026, 1, 3)
        assert count_business_days(start, end, calendar="America/Argentina") == 1

    def test_full_week(self, monday: Date) -> None:
        """Full week Mon-Sun = 5 business days."""
        sunday = _d(2026, 1, 11)
        assert count_business_days(monday, sunday) == 5


# ==============================================================
# count_weekends
# ==============================================================


class TestCountWeekends:
    """Tests for count_weekends."""

    def test_full_week(self, monday: Date, next_monday: Date) -> None:
        """Mon Jan 5 to Mon Jan 12 = 2 weekend days (Sat+Sun)."""
        assert count_weekends(monday, next_monday) == 2

    def test_saturday_to_monday(self, saturday: Date, next_monday: Date) -> None:
        """Sat Jan 10 to Mon Jan 12 = 2 (Sat and Sun)."""
        assert count_weekends(saturday, next_monday) == 2

    def test_no_weekends(self, monday: Date, saturday: Date) -> None:
        """Mon Jan 5 to Sat Jan 10 (exclusive) = 0 weekend days."""
        assert count_weekends(monday, saturday) == 0

    def test_two_weeks(self, monday: Date) -> None:
        """Two full weeks = 4 weekend days."""
        two_weeks_later = _d(2026, 1, 19)
        assert count_weekends(monday, two_weeks_later) == 4


# ==============================================================
# count_holidays
# ==============================================================


class TestCountHolidays:
    """Tests for count_holidays."""

    def test_no_calendar_returns_zero(self, monday: Date, friday: Date) -> None:
        """Without calendar, count is always 0."""
        assert count_holidays(monday, friday) == 0

    def test_argentina_january_one_holiday(self) -> None:
        """Argentina Jan 1-31 2026: only Jan 1 = 1 holiday."""
        start = _d(2026, 1, 1)
        end = _d(2026, 1, 31)
        assert count_holidays(start, end, calendar="America/Argentina") == 1

    def test_argentina_no_holidays_in_range(self) -> None:
        """Argentina Jan 2-10 2026: no holidays."""
        start = _d(2026, 1, 2)
        end = _d(2026, 1, 10)
        assert count_holidays(start, end, calendar="America/Argentina") == 0

    def test_argentina_full_year(self) -> None:
        """Argentina 2026: 15 holidays total."""
        start = _d(2026, 1, 1)
        end = _d(2027, 1, 1)
        assert count_holidays(start, end, calendar="America/Argentina") == 15


# ==============================================================
# time_until_weekend
# ==============================================================


class TestTimeUntilWeekend:
    """Tests for time_until_weekend."""

    @pytest.mark.parametrize(
        "day, expected",
        [
            (5, 5),  # Monday -> 5 days to Saturday
            (6, 4),  # Tuesday
            (7, 3),  # Wednesday
            (8, 2),  # Thursday
            (9, 1),  # Friday
            (10, 0),  # Saturday (already weekend)
            (11, 0),  # Sunday (already weekend)
        ],
        ids=["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
    )
    def test_days_until_weekend(self, day: int, expected: int) -> None:
        """Verify days until weekend for each day of the week."""
        date = _d(2026, 1, day)
        assert time_until_weekend(date) == expected

    def test_custom_weekend(self) -> None:
        """With custom weekend {4, 5}, Friday is 0 days away."""
        custom_weekend = frozenset({4, 5})
        friday = _d(2026, 1, 9)
        assert time_until_weekend(friday, weekend=custom_weekend) == 0

    def test_custom_weekend_from_monday(self) -> None:
        """With custom weekend {4, 5}, Monday is 4 days from Friday."""
        custom_weekend = frozenset({4, 5})
        monday = _d(2026, 1, 5)
        assert time_until_weekend(monday, weekend=custom_weekend) == 4


# ==============================================================
# time_until_business_day
# ==============================================================


class TestTimeUntilBusinessDay:
    """Tests for time_until_business_day."""

    def test_already_business_day(self, monday: Date) -> None:
        """Monday is already a business day, returns 0."""
        assert time_until_business_day(monday) == 0

    def test_saturday_to_monday(self, saturday: Date) -> None:
        """Saturday -> 2 days until Monday."""
        assert time_until_business_day(saturday) == 2

    def test_sunday_to_monday(self, sunday: Date) -> None:
        """Sunday -> 1 day until Monday."""
        assert time_until_business_day(sunday) == 1

    def test_holiday_with_calendar(self) -> None:
        """Jan 1 2026 (Thu, AR holiday) -> 1 day until Jan 2 (Fri)."""
        jan1 = _d(2026, 1, 1)
        result = time_until_business_day(jan1, calendar="America/Argentina")
        assert result == 1

    def test_friday_is_zero(self, friday: Date) -> None:
        """Friday is a business day, returns 0."""
        assert time_until_business_day(friday) == 0
