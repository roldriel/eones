"""core.calendar.py"""

from __future__ import annotations

import calendar
import re
from datetime import datetime
from typing import Dict


class DeltaCalendar:
    """
    Represents calendar-based deltas using months and years.

    Unlike timedelta-based durations, this class handles logical time shifts
    such as "add 1 month" or "add 2 years", accounting for month boundaries
    and varying month lengths.

    Internally, it normalizes the delta into absolute months and reconstructs
    years and months from that total.

    Examples:
        >>> DeltaCalendar(years=1, months=2)
        >>> DeltaCalendar.from_iso("P1Y2M")

    Notes:
        The day component of the input datetime may be truncated if the
        target month has fewer days.
    """

    def __init__(self, years: int = 0, months: int = 0) -> None:
        """
        Initialize a calendar-based delta.

        Args:
            years (int): Number of years to shift.
            months (int): Number of months to shift.

        Raises:
            TypeError: If any input is not an `int` or is a `bool`.
        """
        for name, value in {"years": years, "months": months}.items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"'{name}' must be int, got {type(value).__name__}")

        self._input = {"years": years, "months": months}
        total_months = years * 12 + months
        self.years = total_months // 12
        self.months = total_months % 12

    def apply(self, base_datetime: datetime) -> datetime:
        """
        Apply the calendar delta to a datetime.

        Shifts the month and year while preserving the day when possible.
        If the resulting month has fewer days, the day is truncated.

        Args:
            base_datetime (datetime): The original datetime.

        Returns:
            datetime: A new datetime with the delta applied.
        """
        total_months = base_datetime.year * 12 + base_datetime.month - 1
        total_months += self.years * 12 + self.months
        new_year = total_months // 12
        new_month = (total_months % 12) + 1
        new_day = min(base_datetime.day, calendar.monthrange(new_year, new_month)[1])
        return base_datetime.replace(year=new_year, month=new_month, day=new_day)

    def invert(self) -> "DeltaCalendar":
        """
        Return a new DeltaCalendar with reversed direction.

        Returns:
            DeltaCalendar: The inverse calendar delta.
        """
        return DeltaCalendar(**{k: -v for k, v in self.to_input_dict().items()})

    def scale(self, factor: int) -> "DeltaCalendar":
        """
        Multiply the delta by a scalar.

        Args:
            factor (int): Multiplier.

        Returns:
            DeltaCalendar: A new scaled instance.
        """
        items = self.to_input_dict().items()
        return DeltaCalendar(**{k: v * factor for k, v in items})

    def to_dict(self) -> Dict[str, int]:
        """
        Return a normalized version of the delta.

        This version reflects the internal normalized representation
        (e.g., years=1, months=13 → years=2, months=1).

        Returns:
            Dict[str, int]: Keys are "years" and "months".
        """
        return {"years": self.years, "months": self.months}

    def to_input_dict(self) -> Dict[str, int]:
        """
        Return the original input as passed by the user.

        Returns:
            Dict[str, int]: The original unnormalized dictionary.
        """
        return self._input.copy()

    def is_zero(self) -> bool:
        """
        Check if the delta represents no change.

        Returns:
            bool: True if both years and months are 0.
        """
        return self.years == 0 and self.months == 0

    def __eq__(self, other: object) -> bool:
        """
        Compare two DeltaCalendar instances.

        Returns:
            bool: True if both represent the same normalized delta.
        """
        if not isinstance(other, DeltaCalendar):
            return False

        return (self.years, self.months) == (other.years, other.months)

    def __repr__(self) -> str:
        """
        Return a debug string representation.

        Returns:
            str: e.g., 'DeltaCalendar(years=1, months=2)'
        """
        return f"DeltaCalendar(years={self.years}, months={self.months})"

    def to_iso(self) -> str:
        """
        Serialize to ISO 8601 calendar duration.

        Returns:
            str: ISO representation (e.g., 'P1Y2M').
        """
        parts = []
        if self.years:
            parts.append(f"{self.years}Y")

        if self.months:
            parts.append(f"{self.months}M")

        return "P" + "".join(parts) if parts else "P0M"

    @classmethod
    def from_iso(cls, iso: str) -> "DeltaCalendar":
        """
        Parse an ISO 8601 calendar delta string.

        Args:
            iso (str): ISO string.

        Returns:
            DeltaCalendar: Parsed instance.

        Raises:
            ValueError: If the string is not valid ISO format.
        """
        match = re.fullmatch(r"P(?:(\d+)Y)?(?:(\d+)M)?", iso)
        if not match:
            raise ValueError(f"Invalid ISO calendar delta: {iso}")

        years = int(match.group(1)) if match.group(1) else 0
        months = int(match.group(2)) if match.group(2) else 0
        return cls(years=years, months=months)
