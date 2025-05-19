"""
The temporal façade.

This module defines the Eones class, a high-level entrypoint for working with dates
using expressive operations. It unifies parsing, time shifts, comparisons, and range
generation under a cohesive interface that mirrors human understanding of time.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Literal, Optional, Union

from eones.core.date import EonesDate
from eones.core.delta import EonSpan
from eones.core.parser import Chronologer
from eones.core.range import EonFrame

EonesLike = Union[str, datetime, Dict[str, int], EonesDate]


class Eones:
    """
    Central entrypoint for time manipulation, reasoning, and exploration.

    Acts as a façade for EonesDate and its helpers — abstracting parsing, formatting,
    delta application, comparisons, and range boundaries. A natural interface for working
    with time as a concept, not just a datatype.
    """

    def __init__(
        self,
        value: Optional[Union[str, Dict[str, int], datetime]] = None,
        tz: str = "UTC",
        formats: Optional[List[str]] = None,
    ):
        """Initialize a Eones instance.

        Args:
            value: The initial date (string, dict or datetime).
            tz: Timezone for this date.
            formats: List of string formats for parsing if input is string.
        """
        self._parser = Chronologer(tz=tz, formats=formats)
        self._date = self._parser.parse(value)

    def __repr__(self) -> str:
        """Return a debug-friendly string representation of the Eones instance.

        Returns:
            str: Representation showing date and timezone.
        """
        dt = self._date.to_datetime()
        return f"Eones(date={dt.isoformat()}, " f"tz='{dt.tzinfo}')"

    def __eq__(self, other: object) -> bool:
        """Check equality with another Eones instance.

        Args:
            other (object): Object to compare.

        Returns:
            bool: True if both represent the same date and timezone.
        """
        if not isinstance(other, Eones):
            return False

        return self._date == other._date

    def now(self) -> EonesDate:
        """Return the current internal EonesDate.

        Returns:
            EonesDate: The current date object.
        """
        return self._date

    def add(self, **kwargs: int) -> None:
        """Add a delta to the current date.

        Accepts keyword arguments such as: years, months, days, hours, minutes, seconds.
        Updates the internal EonesDate in place.

        Args:
            **kwargs: Components of the time delta.
        """
        delta = EonSpan(**kwargs)
        self._date = delta.apply(self._date)

    def format(self, fmt: str) -> str:
        """Return the current date formatted using the given format string.

        Args:
            fmt: Format string compatible with datetime.strftime.

        Returns:
            str: Formatted date string.
        """
        return self._date.format(fmt)

    def difference(
        self,
        other: Union["Eones", "EonesDate", str, dict, datetime],
        unit: Literal["days", "months", "years"] = "days",
    ) -> int:
        """
        Compute the difference between this date and another object in the specified unit.

        Args:
            other: A compatible date-like object (EonesDate, Eones, str, dict, datetime).
            unit: Unit for comparison. One of 'days', 'months', or 'years'.

        Returns:
            int: The absolute difference in the specified unit.

        Raises:
            ValueError: If the unit is unsupported.
        """
        if isinstance(other, Eones):
            other_parsed = other.now()

        elif isinstance(other, EonesDate):
            other_parsed = other

        else:
            other_parsed = self._parser.parse(other)

        return self._date.diff(other_parsed, unit)

    def replace(self, **kwargs: int) -> None:
        """Replace date parts of the internal EonesDate.

        Example: replace(day=1, month=1) sets the date to January 1st of same year.

        Args:
            **kwargs: Components to replace (year, month, day, etc).
        """
        self._date = self._date.replace(**kwargs)

    def is_between(
        self, start: EonesLike, end: EonesLike, inclusive: bool = True
    ) -> bool:
        """Check if the current date is between two given dates.

        Args:
            start: Start date (EonesDate, str, dict, datetime).
            end: End date (same formats as start).
            inclusive: Whether to include the endpoints.

        Returns:
            bool: True if the current date is between start and end.
        """
        start_dt = self._parser.parse(start).to_datetime()
        end_dt = self._parser.parse(end).to_datetime()
        return self._date.is_between(start_dt, end_dt, inclusive=inclusive)

    def is_same_week(self, other: EonesLike) -> bool:
        """Return True if this date and the other are in the same ISO week.

        Args:
            other: Another date in any supported input format.

        Returns:
            bool: True if they share the same ISO week and year.
        """
        other_parsed = self._parser.parse(other)
        return self._date.is_same_week(other_parsed)

    def next_weekday(self, weekday: int) -> EonesDate:
        """Get the next occurrence of a given weekday from the current date.

        Args:
            weekday: Integer (0=Monday, ..., 6=Sunday).

        Returns:
            EonesDate: A new EonesDate representing that next weekday.
        """
        return self._date.next_weekday(weekday)

    def is_within(
        self,
        compare: EonesLike,
        check_month: bool = True,
    ) -> bool:
        """Check if current date is within same month/year as 'compare'.

        Args:
            compare: The other date to compare against.
            check_month: Whether to compare month and year (True) or just year (False).

        Returns:
            bool: True if in same period.
        """
        if isinstance(compare, EonesDate):
            return self._date.is_within(compare, check_month=check_month)

        return self._date.is_within(
            self._parser.parse(compare), check_month=check_month
        )

    def range(self, mode: str = "month") -> tuple[datetime, datetime]:
        """Return the datetime range for the given period.

        Args:
            mode: One of "day", "month", or "year".

        Returns:
            Tuple[datetime, datetime]: Start and end datetimes for the period.

        Raises:
            ValueError: If the mode is invalid.
        """
        r = EonFrame(self._date)
        if mode == "day":
            return r.day_range()

        if mode == "month":
            return r.month_range()

        if mode == "year":
            return r.year_range()
        raise ValueError("Invalid range mode. Choose from: day, month, year.")
