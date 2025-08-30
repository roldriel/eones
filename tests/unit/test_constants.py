"""Tests for constants module."""

import pytest

from eones.constants import (
    FIRST_DAY_OF_WEEK,
    is_weekend_day,
    iso_to_us_weekday,
    us_to_iso_weekday,
)


class TestWeekdayConversion:
    """Test weekday conversion functions."""

    @pytest.mark.parametrize(
        "iso_weekday, expected_us_weekday",
        [
            (0, 1),  # Monday -> Monday
            (1, 2),  # Tuesday -> Tuesday
            (2, 3),  # Wednesday -> Wednesday
            (3, 4),  # Thursday -> Thursday
            (4, 5),  # Friday -> Friday
            (5, 6),  # Saturday -> Saturday
            (6, 0),  # Sunday -> Sunday
        ],
    )
    def test_iso_to_us_weekday(self, iso_weekday, expected_us_weekday):
        """Test conversion from ISO weekday to US weekday."""
        assert iso_to_us_weekday(iso_weekday) == expected_us_weekday

    @pytest.mark.parametrize(
        "us_weekday, expected_iso_weekday",
        [
            (0, 6),  # Sunday -> Sunday
            (1, 0),  # Monday -> Monday
            (2, 1),  # Tuesday -> Tuesday
            (3, 2),  # Wednesday -> Wednesday
            (4, 3),  # Thursday -> Thursday
            (5, 4),  # Friday -> Friday
            (6, 5),  # Saturday -> Saturday
        ],
    )
    def test_us_to_iso_weekday(self, us_weekday, expected_iso_weekday):
        """Test conversion from US weekday to ISO weekday."""
        assert us_to_iso_weekday(us_weekday) == expected_iso_weekday

    def test_conversion_roundtrip(self):
        """Test that conversion functions are inverse of each other."""
        for iso_day in range(7):
            us_day = iso_to_us_weekday(iso_day)
            converted_back = us_to_iso_weekday(us_day)
            assert converted_back == iso_day

        for us_day in range(7):
            iso_day = us_to_iso_weekday(us_day)
            converted_back = iso_to_us_weekday(iso_day)
            assert converted_back == us_day


class TestWeekendDetection:
    """Test weekend detection function."""

    @pytest.mark.parametrize(
        "weekday, first_day_of_week, expected",
        [
            # ISO standard (Monday first)
            (0, 0, False),  # Monday
            (1, 0, False),  # Tuesday
            (2, 0, False),  # Wednesday
            (3, 0, False),  # Thursday
            (4, 0, False),  # Friday
            (5, 0, True),  # Saturday
            (6, 0, True),  # Sunday
            # US standard (Sunday first) - weekend is Fri/Sat
            (0, 6, False),  # Monday
            (1, 6, False),  # Tuesday
            (2, 6, False),  # Wednesday
            (3, 6, False),  # Thursday
            (4, 6, True),  # Friday
            (5, 6, True),  # Saturday
            (6, 6, False),  # Sunday
        ],
    )
    def test_is_weekend_day(self, weekday, first_day_of_week, expected):
        """Test weekend detection with different first day of week settings."""
        assert is_weekend_day(weekday, first_day_of_week) == expected

    def test_is_weekend_day_default(self):
        """Test weekend detection with default first day of week."""
        # Should use FIRST_DAY_OF_WEEK constant
        assert is_weekend_day(5) == True  # Saturday
        assert is_weekend_day(6) == True  # Sunday
        assert is_weekend_day(0) == False  # Monday
        assert is_weekend_day(4) == False  # Friday


class TestConstants:
    """Test constants values."""

    def test_first_day_of_week_default(self):
        """Test that FIRST_DAY_OF_WEEK has expected default value."""
        assert FIRST_DAY_OF_WEEK == 0  # ISO standard (Monday)
