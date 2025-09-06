"""contants.py"""

# Default date formats (ISO and common human-readable)
DEFAULT_FORMATS = [
    "%Y-%m-%d",  # 2025-06-15
    "%d/%m/%Y",  # 15/06/2025
    "%Y/%m/%d",  # 2025/06/15
    "%d-%m-%Y",  # 15-06-2025
    "%d.%m.%Y",  # 15.06.2025
    "%Y-%m-%d %H:%M:%S",  # 2025-06-15 13:45:00
    "%d/%m/%Y %H:%M:%S",  # 15/06/2025 13:45:00
    "%Y-%m-%dT%H:%M:%S",  # 2025-06-15T13:45:00 (ISO sin tz)
    "%Y-%m-%dT%H:%M",  # 2025-06-15T13:45
    "%Y-%m-%d %H:%M",  # 2025-06-15 13:45
    "%d %b %Y",  # 15 Jun 2025
    "%d %B %Y",  # 15 June 2025
    "%Y%m%d",  # 20250615
    "%d%m%Y",  # 15062025
    "%Y-%m-%dT%H:%M:%S.%f",  # 2025-06-15T13:45:00.000
    "%Y-%m-%dT%H:%M:%S.%fZ",  # 2025-06-15T13:45:00.000Z
    "%Y-%m-%dT%H:%M:%SZ",  # 2025-06-15T13:45:00Z
    "%Y-%m-%dT%H:%M:%S%z",  # 2025-06-15T13:45:00+0300
    "%Y-%m-%dT%H:%M:%S.%f%z",  # 2025-06-15T13:45:00.123456+0300
    "%a %b %d %H:%M:%S %Y",  # Mon Jun 15 13:45:00 2025
]

# Default timezone
DEFAULT_TIMEZONE = "UTC"

# Valid keys for datetime dictionary parsing
VALID_KEYS = {"year", "month", "day", "hour", "minute", "second", "microsecond"}

# Valid fields for delta specification
DELTA_KEYS = {"years", "months", "weeks", "days", "hours", "minutes", "seconds"}

# First day of the week configuration
# 0 = Monday (ISO standard), 6 = Sunday (US standard)
FIRST_DAY_OF_WEEK = 0  # Default to ISO standard (Monday)


def iso_to_us_weekday(iso_weekday: int) -> int:
    """Convert ISO weekday (0=Monday) to US weekday (0=Sunday).

    Args:
        iso_weekday (int): ISO weekday number (0=Monday, 6=Sunday)

    Returns:
        int: US weekday number (0=Sunday, 6=Saturday)
    """
    return (iso_weekday + 1) % 7


def us_to_iso_weekday(us_weekday: int) -> int:
    """Convert US weekday (0=Sunday) to ISO weekday (0=Monday).

    Args:
        us_weekday (int): US weekday number (0=Sunday, 6=Saturday)

    Returns:
        int: ISO weekday number (0=Monday, 6=Sunday)
    """
    return (us_weekday + 6) % 7


def is_weekend_day(weekday: int, first_day_of_week: int = FIRST_DAY_OF_WEEK) -> bool:
    """Check if a given weekday is a weekend day.

    Args:
        weekday (int): ISO weekday number (0=Monday, 6=Sunday)
        first_day_of_week (int): First day of week (0=Monday, 6=Sunday)

    Returns:
        bool: True if the weekday is a weekend day
    """
    if first_day_of_week == 0:  # ISO standard (Monday first)
        return weekday in (5, 6)  # Saturday, Sunday
    # US standard (Sunday first)
    return weekday in (4, 5)  # Friday, Saturday in ISO numbering
