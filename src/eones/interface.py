"""interface.py"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union, cast

from eones.constants import DEFAULT_FORMATS
from eones.core.date import Date
from eones.core.delta import Delta
from eones.core.parser import Parser
from eones.core.range import Range
from eones.formats import is_valid_format

EonesLike = Union[str, datetime, Dict[str, int], Date]

# Optimization: Reuse a default parser for standard UTC calls
_DEFAULT_PARSER = None


class Eones:
    """
    Central entrypoint for time manipulation, reasoning, and exploration.
    Acts as a façade for Date and its helpers — abstracting parsing,
    formatting, delta application, comparisons, and range boundaries.
    A natural interface for working with time as a concept, not just a datatype.
    """

    # pylint: disable=too-many-public-methods
    __slots__ = ("_date", "_parser")

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

        # Shared Global Parser Logic
        global _DEFAULT_PARSER  # pylint: disable=global-statement

        if formats or additional_formats:
            # Custom formats case - must create new Parser immediately
            if isinstance(formats, str):
                formats = [formats]

            if isinstance(additional_formats, str):
                additional_formats = [additional_formats]

            if formats:
                resolved_formats = formats
            else:
                resolved_formats = DEFAULT_FORMATS + (additional_formats or [])

            self._parser = Parser(tz=tz, formats=resolved_formats)
            self._date = self._parser.parse(value)

        elif tz == "UTC":
            # Fast path: Standard UTC call, no custom formats

            # Optimization: Inline ISO8601 Check
            # Skip parser for standard ISO strings (YYYY-...)
            # logic: len >= 10, value[4] == '-', value[:4].isdigit()
            if (
                isinstance(value, str)
                and len(value) >= 10
                and value[4] == "-"
                and value[:4].isdigit()
            ):
                self._date = Date.from_iso(value)
                return

            # Lazy default parser usage.
            # Avoid initialization if not strictly needed.

            # If value is None, we just want "now".
            if value is None:
                # Optimization: Date(tz="UTC") is roughly "now"
                self._date = Date(tz="UTC")
                return

            # If we actually need to parse 'value' right now, we need a parser.
            if _DEFAULT_PARSER is None:
                _DEFAULT_PARSER = Parser(tz="UTC", formats=DEFAULT_FORMATS)

            # We don't save self._parser here to keep __init__ fast.
            # We only use the global one to parse 'value'
            self._date = _DEFAULT_PARSER.parse(value)

        else:
            # Custom timezone, standard formats
            # We must init a parser for this specific timezone, but we can do it
            # only if we need to store it? No, if we have a custom timezone,
            # future operations (like is_between) should probably use that timezone.
            # But let's keep it simple: simpler to just init it here for non-UTC cases
            # or refactor logic to rely on date.timezone?

            # Current behavior: create a parser for this instance with that TZ.
            self._parser = Parser(tz=tz, formats=DEFAULT_FORMATS)
            self._date = self._parser.parse(value)

    @property
    def parser(self) -> Parser:
        """Lazy loader for the parser instance."""
        try:
            return self._parser

        except AttributeError:
            # It wasn't set in __init__ (fast path)
            global _DEFAULT_PARSER  # pylint: disable=global-statement
            if _DEFAULT_PARSER is None:
                _DEFAULT_PARSER = Parser(tz="UTC", formats=DEFAULT_FORMATS)

            # Note: We do NOT set self._parser = ... here permanently
            # because we want to keep the object lightweight?
            # Actually, Python "slots" already reserve the space.
            # So setting it caches it for next time.
            self._parser = _DEFAULT_PARSER
            return self._parser

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

    def add(self, **kwargs: int) -> Eones:
        """Add a delta to the current date.

        Accepts keyword arguments such as:
        years, months, days, hours, minutes, seconds.
        Updates the internal Date in place.

        Args:
            **kwargs: Components of the time delta.

        Returns:
            Eones: self, updated.
        """
        delta = Delta(**kwargs)
        self._date = self._date + delta
        return self

    def copy(self) -> Eones:
        """Return a copy of the current Eones instance.

        Returns:
            Eones: A new instance with the same date and configuration.
        """
        new_instance = Eones.__new__(Eones)

        # Copy parser only if it exists
        try:
            new_instance._parser = self._parser  # pylint: disable=protected-access

        except AttributeError:
            pass  # Leave it unset in the new instance too

        new_instance._date = self._date  # pylint: disable=protected-access
        return new_instance

    def clone(self) -> Eones:
        """Alias for copy()."""
        return self.copy()

    def format(self, fmt: str) -> str:
        """Return the current date formatted using the given format string."""
        return self._date.format(fmt)

    def difference(self, other: EonesLike, unit: Optional[str] = None) -> int:
        """Calculate the difference between this date and another.

        Args:
            other: The other date to compare with.
            unit: The unit for the difference calculation.
                Options are 'days', 'weeks', 'months', or 'years'.

        Returns:
            int: The time difference expressed in the specified unit.
        """
        unit_type = Literal["days", "weeks", "months", "years"]
        unit_literal = cast(unit_type, unit or "days")
        return self._date.diff(self._coerce_to_date(other), unit_literal)

    def diff_for_humans(self, other: Any | None = None, locale: str = "en") -> str:
        """Return a human-readable difference between dates."""
        other_date = self._coerce_to_date(other) if other is not None else None
        return self._date.diff_for_humans(other_date, locale=locale)

    def replace(self, **kwargs: Any) -> Eones:
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
        # Use property to ensure parser is loaded
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

        to_return = self._date.is_within(
            self.parser.parse(compare), check_month=check_month
        )
        return to_return

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

        return self.parser.parse(other)

    @staticmethod
    def sanitize_formats(formats: List[Any]) -> List[str]:
        """Remove duplicates and invalid formats from a format list.

        Args:
            formats: List of format strings (may contain duplicates or invalid types)

        Returns:
            List[str]: Clean list of unique format strings
        """
        seen = set()
        result = []

        for fmt in formats:
            if isinstance(fmt, str) and fmt not in seen:
                seen.add(fmt)
                result.append(fmt)

        return result

    @staticmethod
    def is_valid_format(date_str: str, formats: List[str]) -> bool:
        """Check if a date string matches any of the provided formats.

        Args:
            date_str: The date string to validate
            formats: List of accepted datetime format strings

        Returns:
            bool: True if the string matches at least one format
        """
        return is_valid_format(date_str, formats)
