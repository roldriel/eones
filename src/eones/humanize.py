"""src/eones/humanize.py"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, cast

from eones.locales import get_messages

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from eones.core.date import Date

# Time units in descending order: (message key, seconds per unit)
_TIME_UNITS = [
    ("year", 31536000),
    ("month", 2592000),
    ("week", 604800),
    ("day", 86400),
    ("hour", 3600),
    ("minute", 60),
    ("second", 1),
]


def diff_for_humans(
    date: "Date", other: Optional["Date"] = None, locale: str = "en"
) -> str:
    """Return a human-friendly representation of the difference.

    Args:
        date: Base date to describe.
        other: Date to compare against. Defaults to ``Date.now`` in the same
            timezone as ``date``.
        locale: Language key for messages.
    """
    messages = get_messages(locale)

    if other is None:
        from eones.core.date import Date  # pylint: disable=import-outside-toplevel

        other = Date.now(tz=date.timezone, naive="utc")

    diff_seconds = (date.to_datetime() - other.to_datetime()).total_seconds()
    future = diff_seconds > 0
    seconds = abs(int(diff_seconds))

    # Find the appropriate unit and count
    for unit, unit_seconds in _TIME_UNITS:
        if seconds >= unit_seconds:
            count = seconds // unit_seconds
            unit_labels = cast(Tuple[str, str], messages[unit])
            label = unit_labels[0] if count == 1 else unit_labels[1]
            break
    else:
        return str(messages["just_now"])

    # Format the phrase based on locale
    marker = str(messages["future"]) if future else str(messages["past"])
    position = messages.get("position")

    if position == "suffix":
        return f"{count} {label}{marker}"

    if locale == "en":
        return f"{marker} {count} {label}" if future else f"{count} {label} {marker}"

    return f"{marker} {count} {label}"
