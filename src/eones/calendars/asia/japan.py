"""src/eones/calendars/asia/japan.py

Japanese national holiday calendar.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Dict, List, Optional, Tuple

from eones.calendars import HolidayCalendar, _make_date, nth_weekday_of_month
from eones.core.date import Date


def _vernal_equinox(year: int) -> int:
    """Calculate the day of the vernal equinox (春分の日) in March.

    Args:
        year: The calendar year.

    Returns:
        The day of the month for the vernal equinox.
    """
    return int(20.8431 + 0.242194 * (year - 1980)) - int((year - 1980) // 4)


def _autumnal_equinox(year: int) -> int:
    """Calculate the day of the autumnal equinox (秋分の日) in September.

    Args:
        year: The calendar year.

    Returns:
        The day of the month for the autumnal equinox.
    """
    return int(23.2488 + 0.242194 * (year - 1980)) - int((year - 1980) // 4)


class Calendar(HolidayCalendar):
    """Japanese national holiday calendar.

    Includes 16 national holidays and substitute holidays (振替休日).
    If a holiday falls on Sunday, the next Monday becomes a substitute holiday.
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all Japanese national holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing holidays, including substitutes.
        """
        holiday_list = [
            # 元日 (Ganjitsu) - New Year's Day
            _make_date(year, 1, 1),
            # 成人の日 (Seijin no Hi) - Coming of Age Day (2nd Monday of Jan)
            nth_weekday_of_month(year, 1, 0, 2),
            # 建国記念の日 (Kenkoku Kinen no Hi) - National Foundation Day
            _make_date(year, 2, 11),
            # 天皇誕生日 (Tennō Tanjōbi) - Emperor's Birthday
            _make_date(year, 2, 23),
            # 春分の日 (Shunbun no Hi) - Vernal Equinox Day
            _make_date(year, 3, _vernal_equinox(year)),
            # 昭和の日 (Shōwa no Hi) - Showa Day
            _make_date(year, 4, 29),
            # 憲法記念日 (Kenpō Kinenbi) - Constitution Memorial Day
            _make_date(year, 5, 3),
            # みどりの日 (Midori no Hi) - Greenery Day
            _make_date(year, 5, 4),
            # こどもの日 (Kodomo no Hi) - Children's Day
            _make_date(year, 5, 5),
            # 海の日 (Umi no Hi) - Marine Day (3rd Monday of July)
            nth_weekday_of_month(year, 7, 0, 3),
            # 山の日 (Yama no Hi) - Mountain Day
            _make_date(year, 8, 11),
            # 敬老の日 (Keirō no Hi) - Respect for Aged Day (3rd Mon of Sep)
            nth_weekday_of_month(year, 9, 0, 3),
            # 秋分の日 (Shūbun no Hi) - Autumnal Equinox Day
            _make_date(year, 9, _autumnal_equinox(year)),
            # スポーツの日 (Supōtsu no Hi) - Sports Day (2nd Mon of Oct)
            nth_weekday_of_month(year, 10, 0, 2),
            # 文化の日 (Bunka no Hi) - Culture Day
            _make_date(year, 11, 3),
            # 勤労感謝の日 (Kinrō Kansha no Hi) - Labor Thanksgiving Day
            _make_date(year, 11, 23),
        ]

        # Implement substitute holiday rule (振替休日)
        # If a holiday falls on Sunday, add next Monday as substitute
        # Avoid adding duplicates if Monday is already a holiday
        substitutes = []
        holiday_dates = {h.to_datetime().date() for h in holiday_list}
        for holiday in holiday_list:
            if holiday.is_sunday():
                substitute = Date(
                    holiday.to_datetime() + timedelta(days=1), naive="utc"
                )
                substitute_date = substitute.to_datetime().date()
                if substitute_date not in holiday_dates:
                    substitutes.append(substitute)
                    holiday_dates.add(substitute_date)

        return holiday_list + substitutes

    def _get_fixed_holiday_map(self) -> Dict[Tuple[int, int], str]:
        """Return mapping of (month, day) to holiday name for fixed holidays.

        Returns:
            Dictionary mapping (month, day) tuples to holiday names.
        """
        return {
            (1, 1): "元日",
            (2, 11): "建国記念の日",
            (2, 23): "天皇誕生日",
            (4, 29): "昭和の日",
            (5, 3): "憲法記念日",
            (5, 4): "みどりの日",
            (5, 5): "こどもの日",
            (8, 11): "山の日",
            (11, 3): "文化の日",
            (11, 23): "勤労感謝の日",
        }

    def _get_movable_holidays(self, year: int) -> Dict[Date, str]:
        """Return mapping of Date to holiday name for movable holidays.

        Args:
            year: The calendar year.

        Returns:
            Dictionary mapping Date objects to holiday names.
        """
        return {
            nth_weekday_of_month(year, 1, 0, 2): "成人の日",
            nth_weekday_of_month(year, 7, 0, 3): "海の日",
            nth_weekday_of_month(year, 9, 0, 3): "敬老の日",
            nth_weekday_of_month(year, 10, 0, 2): "スポーツの日",
        }

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the Japanese holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name in Japanese, or None if not a holiday.
        """
        year = date.year
        month = date.month
        day = date.day

        # Check fixed holidays
        fixed_map = self._get_fixed_holiday_map()
        if (month, day) in fixed_map:
            return fixed_map[(month, day)]

        # Check equinoxes
        if month == 3 and day == _vernal_equinox(year):
            return "春分の日"
        if month == 9 and day == _autumnal_equinox(year):
            return "秋分の日"

        # Check movable holidays
        movable_map = self._get_movable_holidays(year)
        if date in movable_map:
            return movable_map[date]

        # Check for substitute holiday (振替休日)
        prev_day = Date(date.to_datetime() - timedelta(days=1), naive="utc")
        if prev_day.is_sunday():
            prev_name = self.holiday_name(prev_day)
            if prev_name is not None:
                return f"{prev_name}（振替休日）"

        return None
