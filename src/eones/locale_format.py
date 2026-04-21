"""src/eones/locale_format.py"""

from __future__ import annotations

import re

from eones.locales import get_locale_data

# Regex with longest tokens first so the alternation matches greedily
_TOKEN_RE = re.compile(r"MMMM|MMM|dddd|ddd|DD|YYYY|YY|MM|HH|mm|ss|D|M")


# pylint: disable=too-many-arguments, too-many-positional-arguments
def format_locale(
    year: int,
    month: int,
    day: int,
    weekday: int,
    hour: int,
    minute: int,
    second: int,
    fmt: str,
    locale: str = "en",
) -> str:
    """Format date components using locale-aware month/day names.

    Supported tokens (matched longest-first via regex):
        MMMM  - Full month name ("enero", "January")
        MMM   - Abbreviated month name ("ene", "Jan")
        dddd  - Full day name ("lunes", "Monday")
        ddd   - Abbreviated day name ("lun", "Mon")
        DD    - Zero-padded day (01-31)
        D     - Day without padding (1-31)
        MM    - Zero-padded month number (01-12)
        M     - Month number without padding (1-12)
        YYYY  - Four-digit year
        YY    - Two-digit year
        HH    - Zero-padded hour (00-23)
        mm    - Zero-padded minute (00-59)
        ss    - Zero-padded second (00-59)

    Args:
        year: Year component.
        month: Month (1-12).
        day: Day of month (1-31).
        weekday: ISO weekday (0=Monday, 6=Sunday).
        hour: Hour (0-23).
        minute: Minute (0-59).
        second: Second (0-59).
        fmt: Format string with tokens.
        locale: Language code.

    Returns:
        Formatted date string.
    """
    data = get_locale_data(locale)

    token_map = {
        "MMMM": data["months"][month - 1],
        "MMM": data["months_short"][month - 1],
        "dddd": data["days"][weekday],
        "ddd": data["days_short"][weekday],
        "DD": f"{day:02d}",
        "D": str(day),
        "MM": f"{month:02d}",
        "M": str(month),
        "YYYY": f"{year:04d}",
        "YY": f"{year % 100:02d}",
        "HH": f"{hour:02d}",
        "mm": f"{minute:02d}",
        "ss": f"{second:02d}",
    }

    def _replace(match: re.Match[str]) -> str:
        return token_map[match.group()]

    return _TOKEN_RE.sub(_replace, fmt)
