"""
Eones: Navigate time with elegance.

This package provides a semantically rich interface for
handling dates and temporal logic. From parsing and formatting
to complex deltas and period framing, Eones offers tools to  handling
reason about time — not just measure it.
"""

from datetime import datetime, timedelta
from typing import Any, List, Optional, Union

from eones.core.date import Date
from eones.core.parser import Parser
from eones.errors import InvalidFormatError, InvalidTimezoneError
from eones.interface import Eones


# Utility functions for backward compatibility and convenience
def parse_date(
    value: Union[str, dict, datetime],
    tz: str = "UTC",
    formats: Optional[List[str]] = None,
) -> Date:
    """Parse a date from various input formats.

    Args:
        value: Date input (string, dict, or datetime)
        tz: Timezone string
        formats: List of format strings for parsing

    Returns:
        Date: Parsed date object
    """
    # Include common datetime formats including ISO with timezone if none provided
    if formats is None:
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
        ]
    parser = Parser(tz=tz, formats=formats)
    return parser.parse(value)


def format_date(date: Union[Date, datetime], fmt: str) -> str:
    """Format a date using the given format string.

    Args:
        date: Date object or datetime to format
        fmt: Format string

    Returns:
        str: Formatted date string
    """
    if isinstance(date, Date):
        return date.format(fmt)
    if isinstance(date, datetime):
        return date.strftime(fmt)
    raise TypeError(f"Expected Date or datetime object, got {type(date).__name__}")


def add_days(date: Date, days: int) -> Date:
    """Add days to a date.

    Args:
        date: Date object
        days: Number of days to add (can be negative)

    Returns:
        Date: New date with days added
    """
    if not isinstance(date, Date):
        raise ValueError("Expected Date object")
    return date.shift(timedelta(days=days))


def date_diff_days(date1: Date, date2: Date) -> int:
    """Calculate the difference in days between two dates.

    Args:
        date1: First date
        date2: Second date

    Returns:
        int: Difference in days (date2 - date1)
    """
    if not isinstance(date1, Date) or not isinstance(date2, Date):
        raise ValueError("Expected Date objects")
    return (date2.to_datetime() - date1.to_datetime()).days


def date_range(start: Date, end: Date, step_days: int = 1) -> List[Date]:
    """Generate a range of dates from start to end.

    Args:
        start: Start date
        end: End date (inclusive)
        step_days: Step size in days

    Returns:
        List[Date]: List of dates in the range
    """
    if not isinstance(start, Date) or not isinstance(end, Date):
        raise ValueError("Expected Date objects")

    dates = []
    current = start

    while current.to_datetime().date() <= end.to_datetime().date():
        dates.append(current)
        current = current.shift(timedelta(days=step_days))

    return dates


def to_timestamp(date: Union[Date, datetime]) -> int:
    """Convert a date to Unix timestamp.

    Args:
        date: Date object or datetime

    Returns:
        int: Unix timestamp
    """
    if isinstance(date, Date):
        return int(date.to_unix())
    if isinstance(date, datetime):
        return int(date.timestamp())
    raise ValueError("Expected Date or datetime object")


def from_timestamp(timestamp: Union[int, float], tz: str = "UTC") -> Date:
    """Create a Date from Unix timestamp.

    Args:
        timestamp: Unix timestamp (int or float)
        tz: Timezone (default: "UTC")

    Returns:
        Date: Date object
    """
    return Date.from_unix(float(timestamp), tz=tz)


__version__ = "1.4.0"
__all__ = [
    "Eones",
    "InvalidFormatError",
    "InvalidTimezoneError",
    "parse_date",
    "format_date",
    "add_days",
    "date_diff_days",
    "date_range",
    "to_timestamp",
    "from_timestamp",
]
