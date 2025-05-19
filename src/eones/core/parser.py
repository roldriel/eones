"""
The art of interpreting time.

This module defines the Chronologer class, a utility capable of parsing raw date
expressions into EonesDate instances. It bridges human-readable strings and structured
input into structured, timezone-aware temporal objects.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Union
from zoneinfo import ZoneInfo

from eones.constants import VALID_KEYS
from eones.core.date import EonesDate


class Chronologer:
    """
    Converts unshaped temporal input into meaningful EonesDate form.

    Accepts strings, dictionaries, datetimes, or EonesDate instances, and interprets
    them based on provided format patterns. Useful for transforming loose or
    user-provided values into structured time representations.
    """

    def __init__(self, tz: str = "UTC", formats: Optional[List[str]] = None) -> None:
        """Initialize the parser with optional timezone and format list.

        Args:
            tz (str): Timezone string (e.g., 'UTC', 'America/New_York').
            formats (Optional[List[str]]): List of datetime string formats to try.
        """
        self._zone = ZoneInfo(tz)
        self._formats = formats if formats else ["%Y-%m-%d", "%d/%m/%Y"]

    def parse(
        self, value: Union[str, Dict[str, int], datetime, EonesDate, None]
    ) -> EonesDate:
        """Parse an input into a EonesDate.

        Args:
            value: Input value (string, dict, datetime, EonesDate, or None).

        Returns:
            EonesDate: Parsed EonesDate instance.

        Raises:
            ValueError: If input type or content is not valid.
        """
        if value is None:
            return EonesDate(tz=self._zone.key)

        if isinstance(value, datetime):
            return EonesDate(value, self._zone.key)

        if isinstance(value, dict):
            return self._from_dict(value)

        if isinstance(value, EonesDate):
            return value

        if isinstance(value, str):
            return self._from_str(value)

        raise ValueError(f"Unsupported input type: {type(value)}")

    def _from_dict(self, data: Dict[str, int]) -> EonesDate:
        """Build a EonesDate from a dictionary with date parts.

        Args:
            data (Dict[str, int]): Dictionary with keys like 'year', 'month', 'day', etc.

        Returns:
            EonesDate: Parsed date.

        Raises:
            ValueError: If data can't be parsed into a datetime.
        """
        filtered = {k: int(v) for k, v in data.items() if k in VALID_KEYS}
        try:
            dt = datetime(**filtered)
            return EonesDate(dt, self._zone.key)

        except Exception as e:
            raise ValueError(f"Invalid dictionary date input: {e}") from e

    def _from_str(self, date_str: str) -> EonesDate:
        """Parse a string into a EonesDate using known formats.

        Args:
            date_str (str): A date string.

        Returns:
            EonesDate: Parsed date.

        Raises:
            ValueError: If string does not match any known formats.
        """
        for fmt in self._formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return EonesDate(dt.replace(tzinfo=self._zone), self._zone.key)
            except ValueError:
                continue
        raise ValueError(f"Date string '{date_str}' does not match expected formats.")
