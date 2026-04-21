"""src/eones/calendars/america/us.py

US federal holiday calendar.
"""

from __future__ import annotations

from typing import List, Optional

from eones.calendars import (
    HolidayCalendar,
    _make_date,
    last_weekday_of_month,
    nth_weekday_of_month,
)
from eones.core.date import Date


class Calendar(HolidayCalendar):
    """US federal holiday calendar.

    Implements the 11 federal holidays recognized by the United States:
    - New Year's Day (January 1)
    - Martin Luther King Jr. Day (3rd Monday of January)
    - Presidents' Day (3rd Monday of February)
    - Memorial Day (Last Monday of May)
    - Juneteenth National Independence Day (June 19)
    - Independence Day (July 4)
    - Labor Day (1st Monday of September)
    - Columbus Day (2nd Monday of October)
    - Veterans Day (November 11)
    - Thanksgiving Day (4th Thursday of November)
    - Christmas Day (December 25)
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all US federal holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing federal holidays, sorted by date.
        """
        return [
            _make_date(year, 1, 1),  # New Year's Day
            nth_weekday_of_month(year, 1, 0, 3),  # MLK Jr. Day (3rd Monday)
            nth_weekday_of_month(year, 2, 0, 3),  # Presidents' Day (3rd Monday)
            last_weekday_of_month(year, 5, 0),  # Memorial Day (Last Monday)
            _make_date(year, 6, 19),  # Juneteenth
            _make_date(year, 7, 4),  # Independence Day
            nth_weekday_of_month(year, 9, 0, 1),  # Labor Day (1st Monday)
            nth_weekday_of_month(year, 10, 0, 2),  # Columbus Day (2nd Monday)
            _make_date(year, 11, 11),  # Veterans Day
            nth_weekday_of_month(year, 11, 3, 4),  # Thanksgiving (4th Thursday)
            _make_date(year, 12, 25),  # Christmas Day
        ]

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the US federal holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name as a string in English, or None if not a holiday.
        """
        year = date.year
        target = date.to_datetime().date()

        # Movable holidays (computed once)
        mlk_day = nth_weekday_of_month(year, 1, 0, 3).to_datetime().date()
        presidents_day = nth_weekday_of_month(year, 2, 0, 3).to_datetime().date()
        memorial_day = last_weekday_of_month(year, 5, 0).to_datetime().date()
        labor_day = nth_weekday_of_month(year, 9, 0, 1).to_datetime().date()
        columbus_day = nth_weekday_of_month(year, 10, 0, 2).to_datetime().date()
        thanksgiving_day = nth_weekday_of_month(year, 11, 3, 4).to_datetime().date()

        # Build mapping of dates to names for this year
        holiday_map = {
            _make_date(year, 1, 1).to_datetime().date(): "New Year's Day",
            mlk_day: "Martin Luther King Jr. Day",
            presidents_day: "Presidents' Day",
            memorial_day: "Memorial Day",
            _make_date(year, 6, 19)
            .to_datetime()
            .date(): ("Juneteenth National Independence Day"),
            _make_date(year, 7, 4).to_datetime().date(): "Independence Day",
            labor_day: "Labor Day",
            columbus_day: "Columbus Day",
            _make_date(year, 11, 11).to_datetime().date(): "Veterans Day",
            thanksgiving_day: "Thanksgiving Day",
            _make_date(year, 12, 25).to_datetime().date(): "Christmas Day",
        }

        return holiday_map.get(target)
