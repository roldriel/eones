"""src/eones/calendars/europe/spain.py

Spanish national holiday calendar (10 national holidays per Real Decreto).
"""

from __future__ import annotations

from datetime import timedelta
from typing import List, Optional

from eones.calendars import HolidayCalendar, _make_date
from eones.core.date import Date
from eones.core.special_dates import easter_date


class Calendar(HolidayCalendar):
    """Spanish national holiday calendar.

    Contains 10 national holidays as defined by Real Decreto:
    - Año Nuevo (New Year's Day)
    - Epifanía del Señor (Epiphany)
    - Viernes Santo (Good Friday)
    - Fiesta del Trabajo (Labour Day)
    - Asunción de la Virgen (Assumption of Mary)
    - Fiesta Nacional de España (National Day of Spain)
    - Todos los Santos (All Saints' Day)
    - Día de la Constitución (Constitution Day)
    - Inmaculada Concepción (Immaculate Conception)
    - Navidad (Christmas Day)
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all Spanish national holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing Spanish national holidays.
        """
        easter = easter_date(year)
        good_friday = easter.shift(timedelta(days=-2))

        return [
            _make_date(year, 1, 1),  # Año Nuevo
            _make_date(year, 1, 6),  # Epifanía del Señor
            good_friday,  # Viernes Santo
            _make_date(year, 5, 1),  # Fiesta del Trabajo
            _make_date(year, 8, 15),  # Asunción de la Virgen
            _make_date(year, 10, 12),  # Fiesta Nacional de España
            _make_date(year, 11, 1),  # Todos los Santos
            _make_date(year, 12, 6),  # Día de la Constitución
            _make_date(year, 12, 8),  # Inmaculada Concepción
            _make_date(year, 12, 25),  # Navidad
        ]

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the Spanish national holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name in Spanish, or None if not a national holiday.
        """
        year = date.year
        month = date.month
        day = date.day

        # Fixed holidays mapping
        fixed_holidays = {
            (1, 1): "Año Nuevo",
            (1, 6): "Epifanía del Señor",
            (5, 1): "Fiesta del Trabajo",
            (8, 15): "Asunción de la Virgen",
            (10, 12): "Fiesta Nacional de España",
            (11, 1): "Todos los Santos",
            (12, 6): "Día de la Constitución",
            (12, 8): "Inmaculada Concepción",
            (12, 25): "Navidad",
        }

        # Check fixed holidays
        name = fixed_holidays.get((month, day))
        if name:
            return name

        # Easter-based holiday
        easter = easter_date(year)
        good_friday = easter.shift(timedelta(days=-2))
        if date.to_datetime().date() == good_friday.to_datetime().date():
            return "Viernes Santo"

        return None
