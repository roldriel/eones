"""core.delta_duration.py"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Dict


class DeltaDuration:
    """
    Represents a duration-based delta using standard time components.

    This class encapsulates time intervals expressed in weeks, days, hours,
    minutes, and seconds. Internally, it leverages Python's `timedelta` but
    preserves original input granularity for semantic clarity.

    Examples:
        >>> DeltaDuration(days=2, hours=4)
        >>> DeltaDuration.from_iso("P1DT3H")

    Notes:
        - Zero values are excluded from internal state.
        - Input validation ensures only integers are accepted (not bools).
    """

    def __init__(self, **kwargs: int) -> None:
        """
        Initialize a DeltaDuration from keyword arguments.

        Args:
            **kwargs: Components such as weeks, days, hours, minutes, seconds.

        Raises:
            TypeError: If any value is not an `int` or is a `bool`.
        """
        for key, value in kwargs.items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"'{key}' must be int, got {type(value).__name__}")

        self._input = {
            key: value
            for key, value in kwargs.items()
            if key in {"weeks", "days", "hours", "minutes", "seconds"} and value != 0
        }

        self.timedelta = timedelta(
            **{key: self._input.get(key, 0) for key in self._input}
        )

    def apply(self, base_datetime: datetime) -> datetime:
        """
        Apply the duration delta to a given datetime.

        Args:
            base_datetime (datetime): The base datetime to shift.

        Returns:
            datetime: A new datetime offset by this delta.
        """
        return base_datetime + self.timedelta

    def invert(self) -> "DeltaDuration":
        """
        Return a new DeltaDuration with negated values.

        Returns:
            DeltaDuration: The inverse duration.
        """
        return DeltaDuration(**{key: -value for key, value in self._input.items()})

    def to_dict(self) -> Dict[str, int]:
        """
        Return a normalized breakdown of the duration into explicit units.

        Returns:
            Dict[str, int]: Keys are days, hours, minutes, and seconds.
        """
        total_seconds = int(self.timedelta.total_seconds())
        days, remaining_seconds = divmod(total_seconds, 86400)
        hours, remaining_seconds = divmod(remaining_seconds, 3600)
        minutes, seconds = divmod(remaining_seconds, 60)
        return {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}

    def to_input_dict(self) -> Dict[str, int]:
        """
        Return the original dictionary passed to the constructor.

        Returns:
            Dict[str, int]: User-provided keyword arguments (filtered and non-zero).
        """
        return self._input.copy()

    def scale(self, factor: int) -> "DeltaDuration":
        """
        Multiply the duration by a scalar factor.

        Args:
            factor (int): The scaling multiplier.

        Returns:
            DeltaDuration: A new instance with scaled values.
        """
        return DeltaDuration(
            **{key: value * factor for key, value in self._input.items()}
        )

    def is_zero(self) -> bool:
        """
        Check if the duration is equivalent to zero.

        Returns:
            bool: True if total time is 0 seconds.
        """
        return self.timedelta.total_seconds() == 0

    def to_iso(self) -> str:
        """
        Serialize the duration to ISO 8601 format.

        Returns:
            str: ISO 8601-compliant duration string (e.g., 'P1DT2H30M').
        """
        parts = []
        if self.timedelta.days:
            parts.append(f"{self.timedelta.days}D")

        time_parts = []
        total_seconds = self.timedelta.seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            time_parts.append(f"{hours}H")

        if minutes:
            time_parts.append(f"{minutes}M")

        if seconds:
            time_parts.append(f"{seconds}S")

        result = "P" + "".join(parts)
        if time_parts:
            result += "T" + "".join(time_parts)

        return result or "P0D"

    @classmethod
    def from_iso(cls, iso: str) -> "DeltaDuration":
        """
        Parse an ISO 8601 duration string.

        Supports optional weeks (e.g., 'P2W') as per extended ISO 8601.

        Args:
            iso (str): Duration in ISO 8601 format.

        Returns:
            DeltaDuration: Parsed delta instance.

        Raises:
            ValueError: If the format is invalid.
        """
        pattern = r"P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?"
        match = re.fullmatch(pattern, iso)
        if not match:
            raise ValueError(f"Invalid ISO duration: {iso}")

        weeks = int(match.group(1)) if match.group(1) else 0
        days = int(match.group(2)) if match.group(2) else 0
        hours = int(match.group(3)) if match.group(3) else 0
        minutes = int(match.group(4)) if match.group(4) else 0
        seconds = int(match.group(5)) if match.group(5) else 0
        return cls(
            weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
        )
