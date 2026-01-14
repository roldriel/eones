"""src/eones/core/parser.py"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from eones.constants import DEFAULT_FORMATS, VALID_KEYS
from eones.core.date import Date
from eones.errors import InvalidFormatError, InvalidTimezoneError

EonesLike = Union[str, datetime, Dict[str, int], Date]


class Parser:
    """
    Converts unshaped temporal input into meaningful Date form.

    Accepts strings, dictionaries, datetimes, or Date instances, and interprets
    them based on provided format patterns. Useful for transforming loose or
    user-provided values into structured time representations.
    """

    __slots__ = ("_zone", "_formats", "_day_first", "_year_first")

    def __init__(
        self,
        tz: str = "UTC",
        formats: Optional[List[str]] = None,
        day_first: bool = True,
        year_first: bool = True,
    ) -> None:
        """
        Initialize the parser with optional timezone and format list.

        Args:
            tz (str): Timezone string (e.g., 'UTC', 'America/New_York').
            formats (Optional[List[str]]): List of datetime string formats to try.
            day_first (bool): Interpret '10/11' as Nov 10 (True).
            year_first (bool): Interpret '20-01-01' as 2020-01-01 (True).
        """
        try:
            self._zone = ZoneInfo(tz)

        except ZoneInfoNotFoundError as exc:
            raise InvalidTimezoneError(tz) from exc

        # Use centralized default formats from constants
        self._formats = formats if formats else DEFAULT_FORMATS
        self._day_first = day_first
        self._year_first = year_first

    def parse(
        self, value: Union[str, Dict[str, int], datetime, "Date", None]
    ) -> "Date":
        """
        Parse an input into a Date.

        Args:
            value: Input value (string, dict, datetime, Date, or None).

        Returns:
            Date: Parsed Date instance.

        Raises:
            ValueError: If input type or content is not valid.
        """
        if value is None:
            return Date(tz=self._zone.key)

        if isinstance(value, datetime):
            return Date(value, self._zone.key)

        if isinstance(value, dict):
            return self._from_dict(value)

        if isinstance(value, Date):
            return value

        if isinstance(value, str):
            return self._from_str(value)

        raise ValueError(f"Unsupported input type: {type(value)}")

    def _from_dict(self, date_parts: Dict[str, int]) -> "Date":
        """
        Build a Date from a dictionary with date parts.

        Args:
            date_parts (Dict[str, int]): Dictionary with keys like
            'year', 'month', 'day', etc.

        Returns:
            Date: Parsed date.
        """

        invalid_keys = set(date_parts) - VALID_KEYS
        if invalid_keys:
            raise ValueError(f"Invalid date part keys: {sorted(invalid_keys)}")

        now = datetime.now(self._zone)

        parts: Dict[str, Any] = {
            "year": int(date_parts.get("year", now.year)),
            "month": int(date_parts.get("month", now.month)),
            "day": int(date_parts.get("day", now.day)),
            "hour": int(date_parts.get("hour", 0)),
            "minute": int(date_parts.get("minute", 0)),
            "second": int(date_parts.get("second", 0)),
            "microsecond": int(date_parts.get("microsecond", 0)),
            "tzinfo": self._zone,
        }
        return Date(datetime(**parts), tz=self._zone.key)

    def _from_str(self, date_str: str) -> "Date":
        """
        Parse a string into a Date using known formats.

        Args:
            date_str (str): A date string.

        Returns:
            Date: Parsed date.

        Raises:
            ValueError: If string does not match any known formats.
        """
        # Optimization: Try extremely fast ISO parsing first
        # Robust ISO 8601 detection: Starts with YYYY-MM-DD
        try:
            if (
                len(date_str) >= 10
                and date_str[4] == "-"
                and date_str[7] == "-"
                and date_str[:4].isdigit()
            ):
                return Date.from_iso(date_str, self._zone.key)
        except InvalidFormatError:
            # Not a valid ISO structure, fall back to other formats
            pass
        # Note: ValueErrors (logical garbage) bubble up as per contract

        # Adjust formats based on day_first/year_first if they match ambiguous patterns
        # Try matching string against common ambiguous patterns
        # and reorder formats if needed.
        # But a better way is to just use the sorted formats.

        formats_to_try = list(self._formats)

        if not self._day_first:
            # Prioritize MM/DD over DD/MM (US)
            us_formats = ["%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y"]
            for f in reversed(us_formats):
                if f in formats_to_try:
                    formats_to_try.remove(f)
                    formats_to_try.insert(0, f)

        for fmt in formats_to_try:
            try:
                dt = datetime.strptime(date_str, fmt)

                # If the parsed datetime has timezone info, preserve it
                if dt.tzinfo is not None:
                    # Handle timezone-aware datetime - preserve original timezone
                    return Date.from_timezone_aware_datetime(dt)

                # No timezone info, use parser's default timezone
                return Date(dt.replace(tzinfo=self._zone), self._zone.key)

            except ValueError:
                continue

        raise InvalidFormatError(
            f"Date string '{date_str}' does not match expected formats {self._formats}"
        )

    def to_eones_date(self, value: EonesLike) -> Date:
        """
        Convert various types to a Date instance.

        Args:
            value (EonesLike): A value of type Eones, Date, or input parseable to Date.

        Returns:
            Date: Parsed or extracted Date.
        """
        return self.parse(value)
