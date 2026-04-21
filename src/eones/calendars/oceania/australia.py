"""src/eones/calendars/oceania/australia.py"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, List, Optional

from eones.calendars import HolidayCalendar, _make_date, nth_weekday_of_month
from eones.core.special_dates import easter_date

if TYPE_CHECKING:  # pragma: no cover
    from eones.core.date import Date


class Calendar(HolidayCalendar):
    """Australian national public holidays (Fair Work Act 2009).

    Provides the 9 national public holidays observed throughout Australia.
    Note that states and territories may observe additional holidays.
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all national public holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing national public holidays.
        """
        easter = easter_date(year)

        return [
            _make_date(year, 1, 1),  # New Year's Day
            _make_date(year, 1, 26),  # Australia Day
            easter.shift(timedelta(days=-2)),  # Good Friday
            easter.shift(timedelta(days=-1)),  # Easter Saturday
            easter.shift(timedelta(days=1)),  # Easter Monday
            _make_date(year, 4, 25),  # Anzac Day
            nth_weekday_of_month(year, 6, 0, 2),  # Queen's Birthday (2nd Mon)
            _make_date(year, 12, 25),  # Christmas Day
            _make_date(year, 12, 26),  # Boxing Day
        ]

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name as a string, or None if not a holiday.
        """
        year = date.year
        month = date.month
        day = date.day
        target = date.to_datetime().date()

        # Fixed holidays mapping
        fixed_holidays = {
            (1, 1): "New Year's Day",
            (1, 26): "Australia Day",
            (4, 25): "Anzac Day",
            (12, 25): "Christmas Day",
            (12, 26): "Boxing Day",
        }

        if (month, day) in fixed_holidays:
            return fixed_holidays[(month, day)]

        # Easter-based holidays
        easter = easter_date(year)
        easter_holidays = {
            easter.shift(timedelta(days=-2)).to_datetime().date(): "Good Friday",
            easter.shift(timedelta(days=-1)).to_datetime().date(): "Easter Saturday",
            easter.shift(timedelta(days=1)).to_datetime().date(): "Easter Monday",
        }

        if target in easter_holidays:
            return easter_holidays[target]

        # Queen's Birthday (2nd Monday of June)
        queens_birthday = nth_weekday_of_month(year, 6, 0, 2)
        if queens_birthday.to_datetime().date() == target:
            return "Queen's Birthday"

        return None
