"""
Core representation of temporal instants drawn from the fabric of the eons.

This module defines the EonesDate class, a timezone-aware abstraction over Python's
datetime, designed to traverse, transform, and evaluate time with expressive precision.
It supports truncation, rounding, comparison, period bounds, and semantic operations
that bring temporal logic closer to human intuition — yet grounded in rigor.

All moments begin here.
"""

from __future__ import annotations

from calendar import monthrange
from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Optional
from zoneinfo import ZoneInfo

from eones.constants import VALID_KEYS


class EonesDate:
    """
    Encapsulates a precise moment in time, drawn from the infinite thread of eons.

    This class offers a rich set of operations for navigating, formatting, and comparing
    temporal instances, while remaining rooted in timezone-aware datetime logic.
    It bridges raw timekeeping with semantic clarity, allowing you to reason about
    durations, truncations, alignments, and transitions in a way that feels both practical
    and timeless.
    """

    def __init__(self, dt: Optional[datetime] = None, tz: Optional[str] = "UTC"):
        """Initialize a EonesDate object.

        Args:
            dt (datetime, optional): A datetime object. Defaults to current time.
            tz (str, optional): Timezone string. Defaults to "UTC".
        """
        self._zone = ZoneInfo(tz)
        self._dt = dt.astimezone(self._zone) if dt else datetime.now(self._zone)

    def __repr__(self) -> str:
        """Return a string representation of the EonesDate.

        Returns:
            str: Debug-friendly string.
        """
        return f"EonesDate({self._dt.isoformat()})"

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the internal datetime.

        Args:
            name (str): Name of the datetime attribute.

        Returns:
            Any: Value of the corresponding datetime attribute.
        """
        return getattr(self._dt, name)

    def __hash__(self) -> int:
        """Return hash based on the internal datetime.

        Returns:
            int: Hash value.
        """
        return hash(self._dt)

    def __eq__(self, other: object) -> bool:
        """Check equality with another EonesDate.

        Returns:
            bool: True if datetime values are equal.
        """
        if isinstance(other, EonesDate):
            return self._dt == other.to_datetime()

        if isinstance(other, datetime):
            return self._dt == other

        return NotImplemented

    def __str__(self) -> str:
        """Return ISO format string representation.

        Returns:
            str: ISO 8601 datetime string.
        """
        return self._dt.isoformat()

    def copy(self) -> EonesDate:
        """Return a new copy of the current EonesDate.

        Returns:
            EonesDate: A copy of the current date.
        """
        return EonesDate(self._dt, self._zone.key)

    def to_datetime(self) -> datetime:
        """Return the internal datetime object.

        Returns:
            datetime: The timezone-aware datetime.
        """
        return self._dt

    def format(self, fmt: str) -> str:
        """Return formatted datetime as a string.

        Args:
            fmt (str): Datetime format string.

        Returns:
            str: Formatted datetime.
        """
        return self._dt.strftime(fmt)

    def to_iso(self) -> str:
        """Return ISO 8601 formatted string of the datetime.

        Returns:
            str: ISO format datetime string.
        """
        return self._dt.isoformat()

    def to_unix(self) -> float:
        """Return Unix timestamp of the datetime.

        Returns:
            float: Unix timestamp.
        """
        return self._dt.timestamp()

    @classmethod
    def from_iso(cls, iso_str: str, tz: Optional[str] = "UTC") -> EonesDate:
        """Create a EonesDate from an ISO 8601 string.

        Args:
            iso_str (str): ISO date string.
            tz (str, optional): Timezone. Defaults to "UTC".

        Returns:
            EonesDate: Parsed EonesDate.
        """
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo(tz))
        return cls(dt, tz)

    @classmethod
    def from_unix(cls, timestamp: float, tz: Optional[str] = "UTC") -> EonesDate:
        """Create a EonesDate from a Unix timestamp.

        Args:
            timestamp (float): Seconds since epoch.
            tz (str, optional): Timezone. Defaults to "UTC".

        Returns:
            EonesDate: Parsed EonesDate.
        """
        dt = datetime.fromtimestamp(timestamp, tz=ZoneInfo(tz))
        return cls(dt, tz)

    def __lt__(self, other: EonesDate) -> bool:
        """Less-than comparison.

        Returns:
            bool: True if self is before other.
        """
        return self._dt < other.to_datetime()

    def is_within(self, other: EonesDate, check_month: bool = True) -> bool:
        """Check if the current date is within the same year/month as another EonesDate.

        Args:
            other (EonesDate): Date to compare.
            check_month (bool): If True, also check that months match.

        Returns:
            bool: True if within the same period.
        """
        if check_month:
            dt1 = self.to_datetime()
            dt2 = other.to_datetime()
            return dt1.year == dt2.year and dt1.month == dt2.month
        return self.to_datetime().year == other.to_datetime().year

    def is_between(
        self, start: datetime, end: datetime, inclusive: bool = True
    ) -> bool:
        """Check if date is between two datetime bounds.

        Args:
            start (datetime): Start datetime.
            end (datetime): End datetime.
            inclusive (bool): Include boundaries. Defaults to True.

        Returns:
            bool: True if in range.
        """
        if inclusive:
            return start <= self._dt <= end
        return start < self._dt < end

    def is_same_week(self, other: EonesDate) -> bool:
        """Check if two dates fall in the same ISO calendar week.

        Args:
            other (EonesDate): Date to compare.

        Returns:
            bool: True if both dates share the same ISO week.
        """
        return self._dt.isocalendar()[:2] == other.to_datetime().isocalendar()[:2]

    def as_utc(self) -> datetime:
        """Convert to UTC timezone.

        Returns:
            datetime: Datetime in UTC.
        """
        return self._dt.astimezone(timezone.utc)

    def as_local(self, zone: str) -> datetime:
        """Convert to a local timezone.

        Args:
            zone (str): Target timezone name.

        Returns:
            datetime: Datetime in the new timezone.
        """
        return self._dt.astimezone(ZoneInfo(zone))

    def truncate(self, unit: str) -> EonesDate:
        """Truncate the datetime to the start of the specified unit.

        Args:
            unit (str): One of "second", "minute", "hour", "day".

        Returns:
            EonesDate: Truncated datetime.
        """
        dt = self._dt
        if unit == "second":
            return EonesDate(dt.replace(microsecond=0), self._zone.key)

        if unit == "minute":
            return EonesDate(dt.replace(second=0, microsecond=0), self._zone.key)

        if unit == "hour":
            return EonesDate(
                dt.replace(minute=0, second=0, microsecond=0), self._zone.key
            )

        if unit == "day":
            return EonesDate(
                dt.replace(hour=0, minute=0, second=0, microsecond=0), self._zone.key
            )

        raise ValueError("Invalid unit. Use 'second', 'minute', 'hour', or 'day'.")

    def round(self, unit: str) -> EonesDate:
        """Round the datetime to the nearest unit.

        Args:
            unit (str): One of "minute", "hour", or "day".

        Returns:
            EonesDate: Rounded datetime.
        """
        dt = self._dt
        if unit == "minute":
            if dt.second >= 30:
                dt += timedelta(minutes=1)
            return EonesDate(dt.replace(second=0, microsecond=0), self._zone.key)

        if unit == "hour":
            if dt.minute >= 30:
                dt += timedelta(hours=1)
            return EonesDate(
                dt.replace(minute=0, second=0, microsecond=0), self._zone.key
            )

        if unit == "day":
            if dt.hour >= 12:
                dt += timedelta(days=1)
            return EonesDate(
                dt.replace(hour=0, minute=0, second=0, microsecond=0), self._zone.key
            )

        raise ValueError("Invalid unit. Use 'minute', 'hour', or 'day'.")

    def replace(self, **kwargs: Any) -> EonesDate:
        """Return a new EonesDate with replaced datetime fields.

        Allowed fields: year, month, day, hour, minute, second.

        Args:
            **kwargs: Fields to replace in the datetime.

        Returns:
            EonesDate: New date with specified fields replaced.
        """
        filtered = {k: v for k, v in kwargs.items() if k in VALID_KEYS}
        new_dt = self._dt.replace(**filtered)
        return EonesDate(new_dt, self._zone.key)

    def diff(
        self, other: EonesDate, unit: Literal["days", "months", "years"] = "days"
    ) -> int:
        """
        Calculate the absolute difference between this date and another EonesDate
        in the specified unit.

        Args:
            other (EonesDate): The date to compare against.
            unit (str): Unit for comparison: 'days', 'months', or 'years'. Defaults to 'days'.

        Returns:
            int: Absolute difference in the specified unit.

        Raises:
            ValueError: If an unsupported unit is provided.
        """
        self_dt = self.to_datetime()
        other_dt = other.to_datetime()

        if unit == "days":
            return abs((self_dt - other_dt).days)

        if unit == "months":
            years_diff = self_dt.year - other_dt.year
            months_diff = self_dt.month - other_dt.month
            total_months = years_diff * 12 + months_diff
            return abs(total_months)

        if unit == "years":
            return abs(self_dt.year - other_dt.year)

        raise ValueError("Unsupported unit. Use 'days', 'months' or 'years'.")

    def start_of(self, period: str) -> datetime:
        """Return the start of a given period.

        Args:
            period (str): One of 'day', 'week', 'month', or 'year'.

        Returns:
            datetime: Start of the specified period.
        """
        if period == "day":
            return self._dt.replace(hour=0, minute=0, second=0, microsecond=0)

        if period == "week":
            weekday = self._dt.isoweekday()
            return (self._dt - timedelta(days=weekday - 1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        if period == "month":
            return self._dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if period == "year":
            return self._dt.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )

        raise ValueError("Invalid period. Use 'day', 'week', 'month', or 'year'.")

    def end_of(self, period: str) -> datetime:
        """Return the end of a given period.

        Args:
            period (str): One of 'day', 'week', 'month', or 'year'.

        Returns:
            datetime: End of the specified period.
        """
        if period == "day":
            return self._dt.replace(hour=23, minute=59, second=59, microsecond=999999)

        if period == "week":
            weekday = self._dt.isoweekday()
            end_date = self._dt + timedelta(days=7 - weekday)
            return end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        if period == "month":
            last_day = monthrange(self._dt.year, self._dt.month)[1]
            return self._dt.replace(
                day=last_day, hour=23, minute=59, second=59, microsecond=999999
            )

        if period == "year":
            return self._dt.replace(
                month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
            )
        raise ValueError("Invalid period. Use 'day', 'week', 'month', or 'year'.")

    def next_weekday(self, weekday: int) -> EonesDate:
        """Return the next date matching the specified weekday.

        Args:
            weekday (int): Target weekday (0 = Monday).

        Returns:
            EonesDate: The next date matching the weekday.
        """
        current_weekday = self._dt.weekday()
        days_ahead = (weekday - current_weekday + 7) % 7 or 7
        next_date = self._dt + timedelta(days=days_ahead)
        return EonesDate(next_date, self._zone.key)

    def previous_weekday(self, weekday: int) -> EonesDate:
        """Return the previous date matching the specified weekday.

        Args:
            weekday (int): Target weekday (0 = Monday).

        Returns:
            EonesDate: The previous date matching the weekday.
        """
        current_weekday = self._dt.weekday()
        days_behind = (current_weekday - weekday + 7) % 7 or 7
        prev_date = self._dt - timedelta(days=days_behind)
        return EonesDate(prev_date, self._zone.key)
