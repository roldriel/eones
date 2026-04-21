"""src/eones/calendars/europe/germany.py"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, List, Optional

from eones.calendars import HolidayCalendar, _make_date
from eones.core.special_dates import easter_date

if TYPE_CHECKING:  # pragma: no cover
    from eones.core.date import Date


class Calendar(HolidayCalendar):
    """German federal holiday calendar.

    Includes the 9 federal holidays common to all German Bundesländer.
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all German federal holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing federal holidays.
        """
        easter = easter_date(year)

        return [
            _make_date(year, 1, 1),  # Neujahrstag
            easter.shift(timedelta(days=-2)),  # Karfreitag
            easter.shift(timedelta(days=1)),  # Ostermontag
            _make_date(year, 5, 1),  # Tag der Arbeit
            easter.shift(timedelta(days=39)),  # Christi Himmelfahrt
            easter.shift(timedelta(days=50)),  # Pfingstmontag
            _make_date(year, 10, 3),  # Tag der Deutschen Einheit
            _make_date(year, 12, 25),  # 1. Weihnachtstag
            _make_date(year, 12, 26),  # 2. Weihnachtstag
        ]

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the German federal holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name in German, or None if not a federal holiday.
        """
        year = date.year
        dt = date.to_datetime().date()
        easter = easter_date(year)

        holiday_map = {
            _make_date(year, 1, 1).to_datetime().date(): "Neujahrstag",
            easter.shift(timedelta(days=-2)).to_datetime().date(): "Karfreitag",
            easter.shift(timedelta(days=1)).to_datetime().date(): "Ostermontag",
            _make_date(year, 5, 1).to_datetime().date(): "Tag der Arbeit",
            easter.shift(timedelta(days=39))
            .to_datetime()
            .date(): "Christi Himmelfahrt",
            easter.shift(timedelta(days=50)).to_datetime().date(): "Pfingstmontag",
            _make_date(year, 10, 3).to_datetime().date(): "Tag der Deutschen Einheit",
            _make_date(year, 12, 25).to_datetime().date(): "1. Weihnachtstag",
            _make_date(year, 12, 26).to_datetime().date(): "2. Weihnachtstag",
        }

        return holiday_map.get(dt)
