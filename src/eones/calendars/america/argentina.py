"""src/eones/calendars/america/argentina.py"""

from __future__ import annotations

import datetime as _dt
from datetime import timedelta
from typing import Dict, List, Optional

from eones.calendars import HolidayCalendar, _make_date, nth_weekday_of_month
from eones.core.date import Date
from eones.core.special_dates import easter_date


def _pydate(eones_date: Date) -> _dt.date:
    """Convert an Eones Date to a stdlib date for dict keys."""
    return eones_date.to_datetime().date()


class Calendar(HolidayCalendar):
    """Argentina national holiday calendar (Ley 27.399).

    Includes 15 official holidays per year:
    Fixed (9): New Year, Veterans Day, Day of Remembrance, Labor Day,
    May Revolution, Güemes Day, Independence Day, Immaculate Conception,
    Christmas.
    Easter-based (3): Carnival Monday/Tuesday, Good Friday.
    Movable (3): San Martín (3rd Monday of August), Cultural Diversity
    (2nd Monday of October), National Sovereignty (4th Monday of November).
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all official holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing holidays in chronological order.
        """
        easter = easter_date(year)

        return [
            # Fixed holidays
            _make_date(year, 1, 1),  # Año Nuevo
            easter.shift(timedelta(days=-48)),  # Carnaval lunes
            easter.shift(timedelta(days=-47)),  # Carnaval martes
            _make_date(year, 3, 24),  # Día de la Memoria
            _make_date(year, 4, 2),  # Día del Veterano
            easter.shift(timedelta(days=-2)),  # Viernes Santo
            _make_date(year, 5, 1),  # Día del Trabajo
            _make_date(year, 5, 25),  # Revolución de Mayo
            _make_date(year, 6, 17),  # Güemes
            _make_date(year, 7, 9),  # Día de la Independencia
            nth_weekday_of_month(year, 8, 0, 3),  # San Martín (3rd Monday)
            nth_weekday_of_month(year, 10, 0, 2),  # Diversidad (2nd Monday)
            nth_weekday_of_month(year, 11, 0, 4),  # Soberanía (4th Monday)
            _make_date(year, 12, 8),  # Inmaculada Concepción
            _make_date(year, 12, 25),  # Navidad
        ]

    def _holiday_map(self, year: int) -> Dict[_dt.date, str]:
        """Build date-to-name mapping for a given year."""
        easter = easter_date(year)
        return {
            _pydate(_make_date(year, 1, 1)): "Año Nuevo",
            _pydate(easter.shift(timedelta(days=-48))): ("Carnaval (Lunes)"),
            _pydate(easter.shift(timedelta(days=-47))): ("Carnaval (Martes)"),
            _pydate(_make_date(year, 3, 24)): (
                "Día Nacional de la Memoria" " por la Verdad y la Justicia"
            ),
            _pydate(_make_date(year, 4, 2)): (
                "Día del Veterano y de los" " Caídos en la Guerra de Malvinas"
            ),
            _pydate(easter.shift(timedelta(days=-2))): ("Viernes Santo"),
            _pydate(_make_date(year, 5, 1)): ("Día del Trabajo"),
            _pydate(_make_date(year, 5, 25)): ("Día de la Revolución de Mayo"),
            _pydate(_make_date(year, 6, 17)): (
                "Paso a la Inmortalidad del" " General Martín Miguel de Güemes"
            ),
            _pydate(_make_date(year, 7, 9)): ("Día de la Independencia"),
            _pydate(nth_weekday_of_month(year, 8, 0, 3)): (
                "Paso a la Inmortalidad del" " General José de San Martín"
            ),
            _pydate(nth_weekday_of_month(year, 10, 0, 2)): (
                "Día del Respeto a la" " Diversidad Cultural"
            ),
            _pydate(nth_weekday_of_month(year, 11, 0, 4)): (
                "Día de la Soberanía Nacional"
            ),
            _pydate(_make_date(year, 12, 8)): ("Inmaculada Concepción de María"),
            _pydate(_make_date(year, 12, 25)): "Navidad",
        }

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the Spanish name of the holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name in Spanish, or None if not a holiday.
        """
        target = date.to_datetime().date()
        return self._holiday_map(date.year).get(target)
