"""interface.py"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from eones.constants import DEFAULT_FORMATS
from eones.core.date import Date
from eones.core.delta import Delta
from eones.core.parser import Parser
from eones.core.range import Range

EonesLike = Union[str, datetime, Dict[str, int], Date]


class Eones:
    """
    Central entrypoint for time manipulation, reasoning, and exploration.
    Acts as a façade for Date and its helpers — abstracting parsing,
    formatting, delta application, comparisons, and range boundaries.
    A natural interface for working with time as a concept, not just a datatype.
    """

    def __init__(
        self,
        value: Optional[Union[str, Dict[str, int], datetime]] = None,
        tz: str = "UTC",
        formats: Optional[List[str]] = None,
        additional_formats: Optional[List[str]] = None,
    ):
        """Initialize a Eones instance.

        Args:
            value: The initial date (string, dict or datetime).
            tz: Timezone for this date.
            formats: List of string formats for parsing if input is string.
        """
        if formats and additional_formats:
            raise ValueError("Use either 'formats' or 'additional_formats', not both.")

        if isinstance(formats, str):
            formats = [formats]

        if isinstance(additional_formats, str):
            additional_formats = [additional_formats]

        if formats:
            resolved_formats = formats

        elif additional_formats:
            resolved_formats = DEFAULT_FORMATS + additional_formats

        else:
            resolved_formats = DEFAULT_FORMATS

        self._parser = Parser(tz=tz, formats=resolved_formats)
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

    def now(self) -> Date:
        """Return the current internal Date.

        Returns:
            Date: The current date object.
        """
        return self._date

    def add(self, **kwargs: int) -> None:
        """Add a delta to the current date.
        Accepts keyword arguments such as:
        years, months, days, hours, minutes, seconds.
        Updates the internal Date in place.

        Args:
            **kwargs: Components of the time delta.
        """
        delta = Delta(**kwargs)
        self._date = delta.apply(self._date)

    def format(self, fmt: str) -> str:
        """Return the current date formatted using the given format string."""
        return self._date.format(fmt)

    def difference(self, other: Any, unit: Optional[str] = None) -> Delta:
        """Calculate the difference between this date and another.

        Args:
            other (Any): The date to compare with. Can be Eones, Date,
                datetime, dict, or str.
            unit (Optional[str]): The unit of difference to calculate.
                Options are 'days', 'weeks', 'months', or 'years'.

        Returns:
            Delta: The time difference expressed in the specified unit.
        """
        return self._date.diff(self._coerce_to_date(other), unit)

    def diff_for_humans(self, other: Any | None = None, locale: str = "en") -> str:
        """Return a human-readable difference between dates."""
        other_date = self._coerce_to_date(other) if other is not None else None
        return self._date.diff_for_humans(other_date, locale=locale)

    def replace(self, **kwargs: int) -> Eones:
        """
        Replace date parts and update internal Date instance.

        Example: e.replace(day=1, month=1)

        Args:
            **kwargs: Components to replace (year, month, day, etc).

        Returns:
            Eones: self, updated with new internal date.
        """
        self._date = self._date.replace(**kwargs)
        return self

    def floor(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> "Eones":
        """Truncate the current date down to the start of the unit."""
        self._date = self._date.floor(unit)
        return self

    def ceil(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> Eones:
        """
        Advance the current date to the end of the specified temporal unit.

        Args:
            unit (Literal): The unit to ceil to. Valid options are:
                "year", "month", "week", "day", "hour", "minute", "second".

        Returns:
            Eones: The same instance, updated to the ceiled date.
        """
        self._date = self._date.ceil(unit)
        return self

    def is_between(
        self, start: EonesLike, end: EonesLike, inclusive: bool = True
    ) -> bool:
        """
        Check if the current date is between two given dates.

        Args:
            start: Start date (str, dict, datetime, or Date).
            end: End date (same formats as start).
            inclusive: Whether to include the endpoints.

        Returns:
            bool: True if the current date is between start and end.
        """
        parser = Parser(self._date.timezone)
        start_date = parser.parse(start)
        end_date = parser.parse(end)
        return self._date.is_between(
            start_date.to_datetime(), end_date.to_datetime(), inclusive=inclusive
        )

    def is_same_week(self, other: Any) -> bool:
        """Check if another date falls within the same ISO week as this one.

        Args:
            other (Any): The date to compare with. Can be Eones, Date,
                datetime, dict, or str.

        Returns:
            bool: True if both dates are in the same ISO week, False otherwise.
        """
        other_parsed = self._coerce_to_date(other)
        return self._date.is_same_week(other_parsed)

    def next_weekday(self, weekday: int) -> "Date":
        """Get the next occurrence of a given weekday from the current date.

        Args:
            weekday: Integer (0=Monday, ..., 6=Sunday).

        Returns:
            Date: A new Date representing that next weekday.
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
        if isinstance(compare, Date):
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
        r = Range(self._date)
        if mode == "day":
            return r.day_range()

        if mode == "month":
            return r.month_range()

        if mode == "year":
            return r.year_range()
        raise ValueError("Invalid range mode. Choose from: day, month, year.")

    def round(self, unit: Literal["minute", "hour", "day"]) -> "Eones":
        """
        Round the datetime to the nearest unit ("minute", "hour", or "day").

        Returns:
            Eones: self, updated.
        """
        self._date = self._date.round(unit)
        return self

    def start_of(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> "Eones":
        """
        Set the datetime to the start of the specified unit.

        Args:
            unit (Literal): Unit to align to.

        Returns:
            Eones: Self, updated.
        """
        self._date = self._date.start_of(unit)
        return self

    def end_of(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> "Eones":
        """
        Set the datetime to the end of the specified unit.

        Args:
            unit (Literal): Unit to align to.

        Returns:
            Eones: Self, updated.
        """
        self._date = self._date.end_of(unit)
        return self

    def _coerce_to_date(self, other) -> "Date":
        if isinstance(other, Eones):
            return other.now()

        if isinstance(other, Date):
            return other

        return self._parser.parse(other)
