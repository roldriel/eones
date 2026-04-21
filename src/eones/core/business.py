"""src/eones/core/business.py"""

from __future__ import annotations

from datetime import timedelta
from typing import FrozenSet, Optional

from eones.core.date import Date

_DEFAULT_WEEKEND: FrozenSet[int] = frozenset({5, 6})


def _is_weekend(date: Date, weekend: FrozenSet[int]) -> bool:
    """Check if a date falls on a weekend day."""
    return date.to_datetime().weekday() in weekend


def _is_holiday(date: Date, calendar: Optional[str]) -> bool:
    """Check if a date is a holiday using the given calendar."""
    if calendar is None:
        return False
    from eones.calendars import get_calendar  # pylint: disable=import-outside-toplevel

    cal = get_calendar(calendar)
    return cal.is_holiday(date)


def is_business_day(
    date: Date,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> bool:
    """Check if a date is a business day.

    Args:
        date: Date to check.
        weekend: Set of weekday numbers considered weekend (0=Mon, 6=Sun).
        calendar: Calendar identifier (e.g., "America/Argentina").

    Returns:
        True if the date is neither a weekend nor a holiday.
    """
    if _is_weekend(date, weekend):
        return False
    if _is_holiday(date, calendar):
        return False
    return True


def next_business_day(
    date: Date,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> Date:
    """Return the next business day after the given date.

    Args:
        date: Starting date.
        weekend: Set of weekday numbers considered weekend.
        calendar: Calendar identifier.

    Returns:
        The next business day.
    """
    current = date.shift(timedelta(days=1))
    while not is_business_day(current, weekend, calendar):
        current = current.shift(timedelta(days=1))
    return current


def previous_business_day(
    date: Date,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> Date:
    """Return the previous business day before the given date.

    Args:
        date: Starting date.
        weekend: Set of weekday numbers considered weekend.
        calendar: Calendar identifier.

    Returns:
        The previous business day.
    """
    current = date.shift(timedelta(days=-1))
    while not is_business_day(current, weekend, calendar):
        current = current.shift(timedelta(days=-1))
    return current


def add_business_days(
    date: Date,
    days: int,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> Date:
    """Add N business days to a date (skipping weekends and holidays).

    Args:
        date: Starting date.
        days: Number of business days to add (can be negative).
        weekend: Set of weekday numbers considered weekend.
        calendar: Calendar identifier.

    Returns:
        Date after adding the specified business days.
    """
    if days < 0:
        return subtract_business_days(date, -days, weekend, calendar)

    current = date
    remaining = days
    while remaining > 0:
        current = current.shift(timedelta(days=1))
        if is_business_day(current, weekend, calendar):
            remaining -= 1
    return current


def subtract_business_days(
    date: Date,
    days: int,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> Date:
    """Subtract N business days from a date.

    Args:
        date: Starting date.
        days: Number of business days to subtract.
        weekend: Set of weekday numbers considered weekend.
        calendar: Calendar identifier.

    Returns:
        Date after subtracting the specified business days.
    """
    current = date
    remaining = days
    while remaining > 0:
        current = current.shift(timedelta(days=-1))
        if is_business_day(current, weekend, calendar):
            remaining -= 1
    return current


def count_business_days(
    start: Date,
    end: Date,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> int:
    """Count business days between two dates (exclusive of end).

    Args:
        start: Start date.
        end: End date.
        weekend: Set of weekday numbers considered weekend.
        calendar: Calendar identifier.

    Returns:
        Number of business days in the range [start, end).
    """
    count = 0
    step = 1 if start.to_datetime() <= end.to_datetime() else -1
    current = start
    target = end.to_datetime().date()

    while current.to_datetime().date() != target:
        if is_business_day(current, weekend, calendar):
            count += 1
        current = current.shift(timedelta(days=step))
    return count


def count_weekends(start: Date, end: Date) -> int:
    """Count weekend days between two dates (exclusive of end).

    Args:
        start: Start date.
        end: End date.

    Returns:
        Number of weekend days (Saturday + Sunday) in [start, end).
    """
    count = 0
    current = start
    target = end.to_datetime().date()

    while current.to_datetime().date() != target:
        if _is_weekend(current, _DEFAULT_WEEKEND):
            count += 1
        current = current.shift(timedelta(days=1))
    return count


def count_holidays(
    start: Date,
    end: Date,
    calendar: Optional[str] = None,
) -> int:
    """Count holidays between two dates (exclusive of end).

    Args:
        start: Start date.
        end: End date.
        calendar: Calendar identifier.

    Returns:
        Number of holidays in the range [start, end).
    """
    if calendar is None:
        return 0

    from eones.calendars import get_calendar  # pylint: disable=import-outside-toplevel

    cal = get_calendar(calendar)
    start_date = start.to_datetime().date()
    end_date = end.to_datetime().date()

    count = 0
    start_year = start.year
    end_year = end.year
    for yr in range(start_year, end_year + 1):
        for holiday in cal.holidays(yr):
            h_date = holiday.to_datetime().date()
            if start_date <= h_date < end_date:
                count += 1
    return count


def time_until_weekend(
    date: Date,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
) -> int:
    """Return number of days until next weekend day.

    Returns 0 if date is already a weekend day.

    Args:
        date: Date to check.
        weekend: Set of weekday numbers considered weekend.

    Returns:
        Days until weekend (0 if already weekend).
    """
    if _is_weekend(date, weekend):
        return 0
    current = date
    days = 0
    while not _is_weekend(current, weekend):
        current = current.shift(timedelta(days=1))
        days += 1
    return days


def time_until_business_day(
    date: Date,
    weekend: FrozenSet[int] = _DEFAULT_WEEKEND,
    calendar: Optional[str] = None,
) -> int:
    """Return number of days until next business day.

    Returns 0 if date is already a business day.

    Args:
        date: Date to check.
        weekend: Set of weekday numbers considered weekend.
        calendar: Calendar identifier.

    Returns:
        Days until business day (0 if already a business day).
    """
    if is_business_day(date, weekend, calendar):
        return 0
    current = date
    days = 0
    while not is_business_day(current, weekend, calendar):
        current = current.shift(timedelta(days=1))
        days += 1
    return days
