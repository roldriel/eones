"""
Temporal displacements across the eons.

This module defines the EonSpan class, which allows calendar-accurate transformations
on EonesDate objects. It supports year/month-based navigation as well as precise
adjustments via seconds, minutes, hours, and days. Designed for composing temporal
shifts that echo across time.
"""

import calendar
from datetime import timedelta
from typing import Any

from eones.core.date import EonesDate


class EonSpan:
    """
    Represents a time shift across calendar and chronological dimensions.

    Combines calendar-aware deltas (years, months) with precise timedelta shifts,
    allowing flexible adjustments over EonesDate objects. Supports bidirectional
    movement through time as well as comparison of temporal distance.
    """

    def __init__(self, *, years: int = 0, months: int = 0, **kwargs: Any) -> None:
        """Initialize a new EonSpan.

        Args:
            years (int): Number of years to offset.
            months (int): Number of months to offset.
            days (int): Number of days to offset.
            hours (int): Number of hours to offset.
            minutes (int): Number of minutes to offset.
            seconds (int): Number of seconds to offset.
        """
        allowed = {"days", "hours", "minutes", "seconds"}
        invalid_keys = set(kwargs) - allowed
        if invalid_keys:
            raise ValueError(
                f"Invalid time arguments: {invalid_keys}. Allowed: {allowed}"
            )

        self.years = years
        self.months = months
        self.timedelta = timedelta(**kwargs)

    def __repr__(self) -> str:
        """Return a string representation of the EonSpan.

        Returns:
            str: A readable representation for debugging.
        """
        return (
            f"EonSpan(years={self.years}, months={self.months}, "
            f"timedelta={self.timedelta})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another EonSpan.

        Args:
            other: Object to compare.

        Returns:
            bool: True if both deltas have the same values.
        """
        if not isinstance(other, EonSpan):
            return False

        return (
            self.years == other.years
            and self.months == other.months
            and self.timedelta == other.timedelta
        )

    def __hash__(self) -> int:
        """Compute hash based on internal components.

        Returns:
            int: Hash value.
        """
        return hash((self.years, self.months, self.timedelta))

    def __str__(self) -> str:
        """Human-readable string representation.

        Returns:
            str: Description of the delta.
        """
        parts = []
        if self.years:
            parts.append(f"{self.years}y")
        if self.months:
            parts.append(f"{self.months}mo")
        td = self.timedelta
        if td.days:
            parts.append(f"{td.days}d")
        seconds = td.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if secs:
            parts.append(f"{secs}s")
        return " ".join(parts) or "0s"

    def apply(self, date: EonesDate) -> EonesDate:
        """Apply the delta to a EonesDate and return the resulting date.

        Args:
            date (EonesDate): The base date to apply the delta to.

        Returns:
            EonesDate: A new date adjusted by the delta.
        """
        dt = date.to_datetime()

        # Convert everything to absolute month count, then back to year/month
        total_months = (dt.year * 12 + dt.month - 1) + self.years * 12 + self.months
        year = total_months // 12
        month = (total_months % 12) + 1

        # Build new datetime with adjusted year/month and apply timedelta
        day = min(dt.day, self._last_day_of_month(year, month))
        new_date = dt.replace(year=year, month=month, day=day)

        # Add timedelta (days, hours, minutes, seconds)
        new_date += self.timedelta

        # Get timezone string safely
        tzname = dt.tzinfo.key if hasattr(dt.tzinfo, "key") else None

        return EonesDate(new_date, tz=tzname)

    @staticmethod
    def _last_day_of_month(year: int, month: int) -> int:
        """Get the last day of a given month and year.

        Args:
            year (int): Year component.
            month (int): Month component.

        Returns:
            int: The last day (e.g., 28–31).
        """
        return calendar.monthrange(year, month)[1]
