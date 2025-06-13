"""core.parser.py"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Union
from zoneinfo import ZoneInfo

from eones.constants import VALID_KEYS
from eones.core.date import Date

EonesLike = Union[str, datetime, Dict[str, int], Date]


class Parser:
    """
    Converts unshaped temporal input into meaningful Date form.

    Accepts strings, dictionaries, datetimes, or Date instances, and interprets
    them based on provided format patterns. Useful for transforming loose or
    user-provided values into structured time representations.
    """

    def __init__(self, tz: str = "UTC", formats: Optional[List[str]] = None) -> None:
        """
        Initialize the parser with optional timezone and format list.

        Args:
            tz (str): Timezone string (e.g., 'UTC', 'America/New_York').
            formats (Optional[List[str]]): List of datetime string formats to try.
        """
        self._zone = ZoneInfo(tz)
        self._formats = formats if formats else ["%Y-%m-%d", "%d/%m/%Y"]

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
        parts = {
            "year": date_parts.get("year", now.year),
            "month": date_parts.get("month", now.month),
            "day": date_parts.get("day", now.day),
            "hour": date_parts.get("hour", 0),
            "minute": date_parts.get("minute", 0),
            "second": date_parts.get("second", 0),
            "microsecond": date_parts.get("microsecond", 0),
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
        for fmt in self._formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return Date(dt.replace(tzinfo=self._zone), self._zone.key)

            except ValueError:
                continue

        raise ValueError(f"Date string '{date_str}' does not match expected formats.")

    def to_eones_date(self, value: EonesLike) -> Date:
        """
        Convert various types to a Date instance.

        Args:
            value (EonesLike): A value of type Eones, Date, or input parseable to Date.

        Returns:
            Date: Parsed or extracted Date.
        """
        return self.parse(value)
