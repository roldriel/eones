"""Utility functions for human-friendly time differences."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from eones.locales import get_messages

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from eones.core.date import Date


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

        other = Date.now(tz=date.timezone)

    diff_seconds = (date.to_datetime() - other.to_datetime()).total_seconds()
    future = diff_seconds > 0
    seconds = abs(int(diff_seconds))

    units = [
        ("year", 31536000),
        ("month", 2592000),
        ("week", 604800),
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    ]

    for unit, unit_seconds in units:
        if seconds >= unit_seconds:
            count = seconds // unit_seconds
            break
    else:
        return messages["just_now"]

    label = messages[unit][0] if count == 1 else messages[unit][1]

    if locale == "en":
        phrase = (
            f"{messages['future']} {count} {label}"
            if future
            else f"{count} {label} {messages['past']}"
        )
    else:
        prefix = messages["future"] if future else messages["past"]
        phrase = f"{prefix} {count} {label}"

    return phrase
