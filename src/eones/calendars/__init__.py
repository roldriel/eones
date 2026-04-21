"""src/eones/calendars/__init__.py"""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache
from importlib import import_module
from typing import Dict, List, Optional, Type
from zoneinfo import ZoneInfo

from eones.core.date import Date

# Cached UTC zone
_UTC_ZONE = ZoneInfo("UTC")


class HolidayCalendar:
    """Base class for country-specific holiday calendars.

    Subclasses must implement ``holidays`` and ``holiday_name``.
    """

    __slots__ = ()

    def holidays(self, year: int) -> List[Date]:
        """Return all holidays for a given year.

        Args:
            year: The calendar year.

        Returns:
            List of Date objects representing holidays.
        """
        raise NotImplementedError

    def is_holiday(self, date: Date) -> bool:
        """Check if a date is a holiday.

        Args:
            date: The date to check.

        Returns:
            True if the date falls on a holiday.
        """
        target = date.to_datetime().date()
        return any(h.to_datetime().date() == target for h in self.holidays(date.year))

    def holiday_name(self, date: Date) -> Optional[str]:
        """Return the name of the holiday, or None.

        Args:
            date: The date to check.

        Returns:
            Holiday name as a string, or None if not a holiday.
        """
        raise NotImplementedError


# --- Helpers for movable holidays ---


def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> Date:
    """Return the nth occurrence of a weekday in a month.

    Args:
        year: Year.
        month: Month (1-12).
        weekday: ISO weekday (0=Monday, 6=Sunday).
        n: Occurrence (1=first, 2=second, ...).

    Returns:
        Date for the nth weekday.

    Raises:
        ValueError: If no such occurrence exists.
    """
    first_day = datetime(year, month, 1, tzinfo=_UTC_ZONE)
    first_weekday = first_day.weekday()
    offset = (weekday - first_weekday) % 7
    day = 1 + offset + 7 * (n - 1)
    result = datetime(year, month, day, tzinfo=_UTC_ZONE)
    if result.month != month:
        raise ValueError(f"No {n}th weekday {weekday} in {year}-{month:02d}")
    return Date(result, naive="utc")


def last_weekday_of_month(year: int, month: int, weekday: int) -> Date:
    """Return the last occurrence of a weekday in a month.

    Args:
        year: Year.
        month: Month (1-12).
        weekday: ISO weekday (0=Monday, 6=Sunday).

    Returns:
        Date for the last weekday occurrence.
    """
    if month == 12:
        next_month_first = datetime(year + 1, 1, 1, tzinfo=_UTC_ZONE)
    else:
        next_month_first = datetime(year, month + 1, 1, tzinfo=_UTC_ZONE)
    last_day = next_month_first - timedelta(days=1)
    offset = (last_day.weekday() - weekday) % 7
    result = last_day - timedelta(days=offset)
    return Date(result, naive="utc")


def _make_date(year: int, month: int, day: int) -> Date:
    """Create a UTC Date from year/month/day components.

    Args:
        year: Year.
        month: Month (1-12).
        day: Day (1-31).

    Returns:
        A Date instance.
    """
    return Date(datetime(year, month, day, tzinfo=_UTC_ZONE), naive="utc")


# --- Registry ---

_CALENDAR_MAP: Dict[str, str] = {
    "America/Argentina": "eones.calendars.america.argentina",
    "America/US": "eones.calendars.america.us",
    "Europe/France": "eones.calendars.europe.france",
    "Europe/Germany": "eones.calendars.europe.germany",
    "Europe/Spain": "eones.calendars.europe.spain",
    "Asia/Japan": "eones.calendars.asia.japan",
    "Oceania/Australia": "eones.calendars.oceania.australia",
}

_CUSTOM_CALENDARS: Dict[str, HolidayCalendar] = {}


@lru_cache(maxsize=None)
def get_calendar(name: str) -> HolidayCalendar:
    """Get calendar instance by hierarchical name. Lazy import.

    Args:
        name: Calendar identifier (e.g., "America/Argentina").

    Returns:
        HolidayCalendar instance.

    Raises:
        ValueError: If calendar name is not registered.
    """
    if name in _CUSTOM_CALENDARS:
        return _CUSTOM_CALENDARS[name]

    module_path = _CALENDAR_MAP.get(name)
    if module_path is None:
        raise ValueError(f"Unknown calendar: {name!r}")

    module = import_module(module_path)
    calendar_class: Type[HolidayCalendar] = getattr(module, "Calendar")
    return calendar_class()


def register_calendar(name: str, calendar_class: Type[HolidayCalendar]) -> None:
    """Register a custom calendar.

    Args:
        name: Hierarchical identifier (e.g., "Custom/MyCompany").
        calendar_class: HolidayCalendar subclass.
    """
    _CUSTOM_CALENDARS[name] = calendar_class()
    get_calendar.cache_clear()


def available_calendars() -> List[str]:
    """Return sorted list of all registered calendar names.

    Returns:
        Sorted list of calendar identifiers.
    """
    all_names = set(_CALENDAR_MAP.keys()) | set(_CUSTOM_CALENDARS.keys())
    return sorted(all_names)
