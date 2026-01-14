"""src/eones/interface.py"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Union,
    cast,
)

from eones.constants import DEFAULT_FORMATS
from eones.core.date import Date
from eones.core.delta import Delta
from eones.core.parser import Parser
from eones.core.range import Range
from eones.core.special_dates import easter_date
from eones.formats import is_valid_format

EonesLike = Union[str, datetime, Dict[str, int], Date]

# Optimization: Reuse a default parser for standard UTC calls
_DEFAULT_PARSER = None


# pylint: disable=too-many-public-methods
class Eones:
    """
    Central entrypoint for time manipulation, reasoning, and exploration.
    Acts as a façade for Date and its helpers — abstracting parsing,
    formatting, delta application, comparisons, and range boundaries.
    A natural interface for working with time as a concept, not just a datatype.
    """

    _date: Date
    _parser: Parser

    __slots__ = ("_date", "_parser")

    # pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-branches
    def __init__(
        self,
        value: Optional[EonesLike] = None,
        tz: str = "UTC",
        formats: Optional[Union[List[str], str]] = None,
        additional_formats: Optional[Union[List[str], str]] = None,
        day_first: bool = True,
        year_first: bool = True,
    ):
        """Initialize a Eones instance."""
        # ULTRA FAST PATH: Default UTC construction with ISO string or None
        if (
            tz == "UTC"
            and day_first
            and year_first
            and not formats
            and not additional_formats
        ):
            if (
                isinstance(value, str)
                and len(value) >= 10
                and value[4] == "-"
                and value[:4].isdigit()
            ):
                self._date = Date.from_iso(value)
                return
            if value is None:
                self._date = Date(tz="UTC")
                return
            if isinstance(value, datetime):
                self._date = Date(value, tz="UTC")
                return

        if formats and additional_formats:
            raise ValueError("Use either 'formats' or 'additional_formats', not both.")

        # VERY FAST PATH: Direct instance injection
        if isinstance(value, Eones):
            self._date = value._date
            self._parser = value._parser
            return

        if isinstance(value, Date):
            self._date = value
            return

        # Initialize core objects
        global _DEFAULT_PARSER  # pylint: disable=global-statement

        if formats or additional_formats:
            # Custom parsing path
            if isinstance(formats, str):
                formats = [formats]
            if isinstance(additional_formats, str):
                additional_formats = [additional_formats]

            resolved_formats = (
                formats if formats else DEFAULT_FORMATS + (additional_formats or [])
            )
            self._parser = Parser(
                tz=tz,
                formats=resolved_formats,
                day_first=day_first,
                year_first=year_first,
            )
            self._date = self._parser.parse(value)
        else:
            # Standard/Default parsing path
            if tz == "UTC" and day_first and year_first:
                if _DEFAULT_PARSER is None:
                    _DEFAULT_PARSER = Parser(tz="UTC", formats=DEFAULT_FORMATS)
                self._parser = _DEFAULT_PARSER
            else:
                self._parser = Parser(
                    tz=tz,
                    formats=DEFAULT_FORMATS,
                    day_first=day_first,
                    year_first=year_first,
                )
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

    def to_datetime(self) -> datetime:
        """Return the underlying datetime object.

        Returns:
            datetime: The internal datetime.
        """
        return self._date.to_datetime()

    def add(
        self, delta: Optional[Union[Delta, timedelta]] = None, **kwargs: int
    ) -> Eones:
        """Add a delta to the current date.

        Accepts either a Delta/timedelta instance or keyword arguments
        (years, months, days, etc.).

        Args:
            delta (Optional[Union[Delta, timedelta]]): Pre-computed delta instance.
            **kwargs: Individual components of the time delta.

        Returns:
            Eones: self, updated.
        """
        if delta is not None:
            if kwargs:
                raise ValueError(
                    "Use either a pre-computed 'delta' or 'kwargs', not both."
                )
            self._date = self._date + delta
        else:
            # Optimization: If only duration fields are used, use timedelta + shift
            # which is significantly faster than creating a Delta instance.
            if kwargs and "months" not in kwargs and "years" not in kwargs:
                self._date = self._date.shift(timedelta(**kwargs))
            else:
                self._date = self._date + Delta(**kwargs)
        return self

    def subtract(
        self, other: Optional[Union[Delta, timedelta]] = None, **kwargs: int
    ) -> Eones:
        """Subtract a delta or other date from the current date.

        Accepts either a Delta/timedelta instance or keyword arguments
        (years, months, days, etc.).

        Args:
            other (Optional[Union[Delta, timedelta]]): Pre-computed delta instance.
            **kwargs: Individual components of the time delta.

        Returns:
            Eones: self, updated.
        """
        if other is not None:
            if kwargs:
                raise ValueError(
                    "Use either a pre-computed 'other' or 'kwargs', not both."
                )
            self._date = cast(Date, self._date - other)
        else:
            # Optimization: Duration-only bypass
            if kwargs and "months" not in kwargs and "years" not in kwargs:
                self._date = self._date.shift(-timedelta(**kwargs))
            else:
                self._date = cast(Date, self._date - Delta(**kwargs))
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

    def for_json(self) -> str:
        """Return ISO 8601 string for JSON serialization.

        Returns:
            str: ISO format datetime string.
        """
        return self._date.for_json()

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

    @staticmethod
    def range_iter(
        start: EonesLike, end: EonesLike, step: Union[Delta, timedelta]
    ) -> Generator[Date, None, None]:
        """Iterate from start to end by step.

        Args:
            start (EonesLike): Starting date.
            end (EonesLike): Ending date.
            step (Union[Delta, timedelta]): Interval between each step.

        Yields:
            Generator[Date, None, None]: Sequence of Date objects.
        """
        parser = Parser()  # Uses default UTC/formats
        start_date = parser.to_eones_date(start)
        end_date = parser.to_eones_date(end)
        return Range.range_iter(start_date, end_date, step)

    @staticmethod
    def easter_date(year: int) -> Date:
        """Calculate the date of Easter Sunday for a given year.

        Args:
            year (int): Year to calculate Easter for.

        Returns:
            Date: Date object representing Easter Sunday.
        """
        return easter_date(year)

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

    def _coerce_to_date(self, other: Any) -> Date:
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
