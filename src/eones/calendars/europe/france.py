"""src/eones/calendars/europe/france.py"""

from __future__ import annotations

from datetime import timedelta
from typing import List, Optional

from eones.calendars import HolidayCalendar, _make_date
from eones.core.date import Date
from eones.core.special_dates import easter_date


class Calendar(HolidayCalendar):
    """French public holiday calendar.

    Implements the 11 official holidays defined in Code du travail,
    article L3133-1.
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all French public holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing French public holidays.
        """
        easter = easter_date(year)

        return [
            # Fixed holidays
            _make_date(year, 1, 1),  # Jour de l'An
            _make_date(year, 5, 1),  # Fête du Travail
            _make_date(year, 5, 8),  # Victoire 1945
            _make_date(year, 7, 14),  # Fête Nationale
            _make_date(year, 8, 15),  # Assomption
            _make_date(year, 11, 1),  # Toussaint
            _make_date(year, 11, 11),  # Armistice
            _make_date(year, 12, 25),  # Noël
            # Movable holidays (Easter-based)
            easter.shift(timedelta(days=1)),  # Lundi de Pâques
            easter.shift(timedelta(days=39)),  # Ascension
            easter.shift(timedelta(days=50)),  # Lundi de Pentecôte
        ]

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the French holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name in French, or None if not a holiday.
        """
        year = date.year
        easter = easter_date(year)

        # Map of date components to holiday names
        dt = date.to_datetime().date()

        # Fixed holidays
        fixed_holidays = {
            (1, 1): "Jour de l'An",
            (5, 1): "Fête du Travail",
            (5, 8): "Victoire 1945",
            (7, 14): "Fête Nationale",
            (8, 15): "Assomption",
            (11, 1): "Toussaint",
            (11, 11): "Armistice",
            (12, 25): "Noël",
        }

        key = (dt.month, dt.day)
        if key in fixed_holidays:
            return fixed_holidays[key]

        # Movable holidays (Easter-based)
        if dt == easter.shift(timedelta(days=1)).to_datetime().date():
            return "Lundi de Pâques"
        if dt == easter.shift(timedelta(days=39)).to_datetime().date():
            return "Ascension"
        if dt == easter.shift(timedelta(days=50)).to_datetime().date():
            return "Lundi de Pentecôte"

        return None
