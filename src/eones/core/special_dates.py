"""src/eones/core/special_dates.py"""

from datetime import datetime

from eones.core.date import Date


def easter_date(year: int) -> Date:
    """Calculate the date of Easter Sunday for a given year.

    Uses the Meeus/Jones/Butcher algorithm.

    Args:
        year (int): The year to calculate Easter for.

    Returns:
        Date: A Date object representing Easter Sunday.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1

    return Date(datetime(year, month, day), naive="utc")
