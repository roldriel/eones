"""core.delta.py"""

import re
from typing import Dict

from eones.constants import DELTA_KEYS
from eones.core.date import Date
from eones.core.delta_calendar import DeltaCalendar
from eones.core.delta_duration import DeltaDuration


class Delta:
    """
    Represents a compound time delta composed of calendar (years, months)
    and duration (weeks, days, hours, minutes, seconds) components.

    Calendar components are applied first, followed by duration components.
    This order preserves intuitive behavior when transitioning across
    irregular month lengths (e.g., Jan 31 + 1 month → Feb 28/29).

    Examples:
        >>> Delta(years=1, days=3)
        >>> Delta.from_iso("P1Y3D")

    Notes:
        The original input dictionary is preserved for accurate inversion and scaling.
    """

    def __init__(self, **kwargs: int) -> None:
        """Initialize a Delta with calendar and/or duration parts."""
        invalid_keys = set(kwargs) - DELTA_KEYS
        if invalid_keys:
            raise ValueError(
                f"Invalid delta fields: {invalid_keys}. Allowed: {sorted(DELTA_KEYS)}"
            )

        for k, v in kwargs.items():
            if not isinstance(v, int) or isinstance(v, bool):
                raise TypeError(f"'{k}' must be int, got {type(v).__name__}")

        self._input = {k: v for k, v in kwargs.items() if v != 0}

        calendar_kwargs = {
            "years": kwargs.get("years", 0),
            "months": kwargs.get("months", 0),
        }

        duration_kwargs = {
            "weeks": kwargs.get("weeks", 0),
            "days": kwargs.get("days", 0),
            "hours": kwargs.get("hours", 0),
            "minutes": kwargs.get("minutes", 0),
            "seconds": kwargs.get("seconds", 0),
        }

        self._calendar = DeltaCalendar(**calendar_kwargs)
        self._duration = DeltaDuration(**duration_kwargs)

    def __repr__(self) -> str:
        if not self._input:
            return "Delta(0s)"
        parts = ", ".join(f"{k}={v}" for k, v in self._input.items())
        return f"Delta({parts})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Delta):
            return False
        return self._calendar == other._calendar and self._duration == other._duration

    def __hash__(self) -> int:
        return hash(
            (self._calendar.years, self._calendar.months, self._duration.timedelta)
        )

    def __str__(self) -> str:
        """
        Return a human-readable string (e.g., '1y 2mo 3d 4h').

        Returns:
            str: Compact description.
        """
        parts = []
        calendar = self._calendar
        duration = self._duration.timedelta

        if calendar.years:
            parts.append(f"{calendar.years}y")
        if calendar.months:
            parts.append(f"{calendar.months}mo")

        if duration.days:
            parts.append(f"{duration.days}d")

        seconds = duration.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if secs:
            parts.append(f"{secs}s")

        return " ".join(parts) or "0s"

    def apply(self, date: Date, calendar: bool = True, duration: bool = True) -> Date:
        """
        Apply this delta to a Date instance.

        Args:
            date (Date): The reference date.
            calendar (bool): Whether to apply calendar delta (years/months).
            duration (bool): Whether to apply duration delta (weeks to seconds).

        Returns:
            Date: A new shifted Date instance.

        Raises:
            TypeError: If input is not a Date.
        """
        if not isinstance(date, Date):
            raise TypeError(
                f"'date' must be a Date instance, got {type(date).__name__}"
            )

        dt = date.to_datetime()
        if calendar:
            dt = self._calendar.apply(dt)
        if duration:
            dt = self._duration.apply(dt)

        tzname = getattr(dt.tzinfo, "key", None) or str(dt.tzinfo)
        return Date(dt, tz=tzname)

    def apply_calendar(self, date: Date) -> Date:
        """
        Apply only the calendar part to a date.

        Args:
            date (Date): The original date.

        Returns:
            Date: Date with years/months applied.
        """
        return self.apply(date, calendar=True, duration=False)

    def apply_duration(self, date: Date) -> Date:
        """
        Apply only the duration part to a date.

        Args:
            date (Date): The original date.

        Returns:
            Date: Date with weeks to seconds applied.
        """
        return self.apply(date, calendar=False, duration=True)

    def invert(self) -> "Delta":
        """
        Return the inverse of this delta.

        Returns:
            Delta: Negated delta.
        """
        return Delta(**{k: -v for k, v in self.to_input_dict().items()})

    def scale(self, factor: int) -> "Delta":
        """
        Multiply the delta by a scalar.

        Args:
            factor (int): Scaling multiplier.

        Returns:
            Delta: A new instance.
        """
        return Delta(**{k: v * factor for k, v in self.to_input_dict().items()})

    def is_zero(self) -> bool:
        """
        Check if the delta has no effect.

        Returns:
            bool: True if delta is zero.
        """
        return not self._input

    def to_dict(self) -> Dict[str, int]:
        """
        Return a normalized dict combining calendar and duration.

        Returns:
            Dict[str, int]: Keys include 'years', 'months', 'days', 'hours', etc.
        """
        return self._calendar.to_dict() | self._duration.to_dict()

    def to_input_dict(self) -> Dict[str, int]:
        """
        Return the original input dictionary.

        Returns:
            Dict[str, int]: User-specified delta components.
        """
        return self._input.copy()

    def to_iso(self) -> str:
        """
        Return ISO 8601-compliant string representation.

        Returns:
            str: Serialized delta (e.g., 'P1Y2M3DT4H30M').
        """
        calendar = self._calendar.to_dict()
        duration = self._duration.to_dict()

        parts = []
        if calendar["years"]:
            parts.append(f"{calendar['years']}Y")

        if calendar["months"]:
            parts.append(f"{calendar['months']}M")

        if duration.get("days"):
            parts.append(f"{duration['days']}D")

        time_parts = []
        if duration.get("hours"):
            time_parts.append(f"{duration['hours']}H")

        if duration.get("minutes"):
            time_parts.append(f"{duration['minutes']}M")

        if duration.get("seconds"):
            time_parts.append(f"{duration['seconds']}S")

        iso = "P" + "".join(parts)
        if time_parts:
            iso += "T" + "".join(time_parts)

        return iso or "P0D"

    @classmethod
    def from_iso(cls, iso: str) -> "Delta":
        """
        Parse ISO 8601 delta string.

        Args:
            iso (str): ISO-compliant duration string.

        Returns:
            Delta: Parsed instance.

        Raises:
            ValueError: If the format is invalid.
        """
        pattern = (
            r"P(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?(?:(?P<days>\d+)D)?"
            r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?"
        )
        match = re.fullmatch(pattern, iso)
        if not match:
            raise ValueError(f"Invalid ISO delta: {iso}")
        parts = {k: int(v) for k, v in match.groupdict().items() if v is not None}
        return cls(**parts)
