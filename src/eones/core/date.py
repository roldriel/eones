"""core.date.py"""

from __future__ import annotations

import re
from calendar import monthrange
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Literal, Optional, Union, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from eones.constants import VALID_KEYS, is_weekend_day
from eones.errors import InvalidFormatError, InvalidTimezoneError
from eones.humanize import diff_for_humans as _diff_for_humans

# Optimization: Cached UTC zone
_UTC_ZONE = ZoneInfo("UTC")

if TYPE_CHECKING:  # pragma: no cover - import for type checking only
    from eones.core.delta import Delta


class Date:  # pylint: disable=too-many-public-methods
    """Time manipulation wrapper for timezone-aware datetime operations."""

    __slots__ = ("_dt", "_zone")

    def __init__(
        self,
        dt: Optional[datetime] = None,
        tz: Optional[str] = "UTC",
        naive: Literal["utc", "local", "raise"] = "raise",
    ):
        if tz is None:
            tz = "UTC"

        try:
            # Optimization: Fast path for UTC
            if tz == "UTC":
                self._zone = _UTC_ZONE
            else:
                self._zone = ZoneInfo(tz)

        except ZoneInfoNotFoundError as exc:
            raise InvalidTimezoneError(tz) from exc

        if dt is None:
            self._dt = datetime.now(self._zone)
            return

        if naive not in {"utc", "local", "raise"}:
            raise ValueError("Invalid 'naive' value. Use 'utc', 'local' or 'raise'.")

        if dt.tzinfo is None:
            if naive == "local":
                dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)

            elif naive == "utc":
                dt = dt.replace(tzinfo=ZoneInfo("UTC"))

            else:
                raise ValueError(
                    "Naive datetime received. "
                    "Use naive='utc' or 'local' to clarify intention."
                )

        self._dt = dt.astimezone(self._zone)

    def __repr__(self) -> str:
        """Return a string representation of the Date.

        Returns:
            str: Debug-friendly string.
        """
        return f"Date({self._dt.isoformat()})"

    def __hash__(self) -> int:
        """Return hash based on the internal datetime.

        Returns:
            int: Hash value.
        """
        return hash(self._dt)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.as_utc() == other.as_utc()
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.as_utc() < other.as_utc()
        return NotImplemented

    def __str__(self) -> str:
        """Return ISO format string representation.

        Returns:
            str: ISO 8601 datetime string.
        """
        return self._dt.isoformat()

    def shift(self, delta: timedelta) -> Date:
        """Return a new Date shifted by the given timedelta."""
        return self._with(self._dt + delta)

    def __add__(self, delta: Union[timedelta, "Delta"]) -> Date:
        """Add a Delta or timedelta to this date."""
        from eones.core.delta import Delta  # pylint: disable=import-outside-toplevel

        if isinstance(delta, Delta):
            return delta.apply(self)

        if isinstance(delta, timedelta):
            return self.shift(delta)

        return NotImplemented

    def __sub__(
        self,
        other: Union[Date, timedelta, "Delta"],
    ) -> Union[Date, timedelta]:
        """Subtract a Date, Delta, or timedelta from this date."""
        from eones.core.delta import Delta  # pylint: disable=import-outside-toplevel

        if isinstance(other, Delta):
            return other.invert().apply(self)

        if isinstance(other, timedelta):
            return self.shift(-other)

        if isinstance(other, Date):
            return self._dt - other.to_datetime()

        return NotImplemented

    @classmethod
    def now(
        cls, tz: str = "UTC", naive: Literal["utc", "local", "raise"] = "raise"
    ) -> Date:
        """Create a Date for the current moment."""
        dt = datetime.now()

        if naive == "utc":
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        elif naive == "local":
            dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)

        elif naive != "raise":
            raise ValueError("Invalid 'naive' value. Use 'utc', 'local', or 'raise'.")

        return cls(dt, tz=tz, naive=naive)

    @property
    def year(self) -> int:
        """Year component of the date."""
        return self._dt.year

    @property
    def month(self) -> int:
        """Month component of the date."""
        return self._dt.month

    @property
    def day(self) -> int:
        """Day component of the date."""
        return self._dt.day

    @property
    def hour(self) -> int:
        """Hour component of the date."""
        return self._dt.hour

    @property
    def minute(self) -> int:
        """Minute component of the date."""
        return self._dt.minute

    @property
    def second(self) -> int:
        """Second component of the date."""
        return self._dt.second

    @property
    def microsecond(self) -> int:
        """Microsecond component of the date."""
        return self._dt.microsecond

    @property
    def timezone(self) -> str:
        """Return the key of the timezone in use."""
        return self._zone.key

    def _replace_fields(self, **kwargs: Any) -> Date:
        return self._with(self._dt.replace(**kwargs))

    def _rounded(self, dt: datetime, unit: str) -> datetime:
        thresholds = {
            "microsecond": lambda d: d.microsecond >= 500_000,
            "second": lambda d: d.microsecond >= 500_000,
            "minute": lambda d: d.second >= 30,
            "hour": lambda d: d.minute >= 30,
            "day": lambda d: d.hour >= 12,
        }

        increments = {
            "microsecond": timedelta(microseconds=1),
            "second": timedelta(seconds=1),
            "minute": timedelta(minutes=1),
            "hour": timedelta(hours=1),
            "day": timedelta(days=1),
        }

        normalizers = {
            "microsecond": lambda d: d.replace(microsecond=0),
            "second": lambda d: d.replace(microsecond=0),
            "minute": lambda d: d.replace(second=0, microsecond=0),
            "hour": lambda d: d.replace(minute=0, second=0, microsecond=0),
            "day": lambda d: d.replace(hour=0, minute=0, second=0, microsecond=0),
        }

        if unit not in thresholds:
            raise ValueError(
                "Invalid unit. Use 'microsecond', 'second', 'minute', 'hour', or "
                "'day'."
            )

        if thresholds[unit](dt):
            dt += increments[unit]

        return normalizers[unit](dt)

    def round(self, unit: str) -> Date:
        """Round the Date to the nearest specified unit."""
        valid_units = {"second", "minute", "hour", "day"}
        if unit not in valid_units:
            raise ValueError(
                f"Unsupported round unit '{unit}'. Valid units: {valid_units}"
            )
        return self._with(self._rounded(self._dt, unit))

    def _with(self, dt: datetime) -> Date:
        return Date(dt=dt, tz=str(self._zone))

    def to_datetime(self) -> datetime:
        """Return the internal datetime object.

        Returns:
            datetime: The timezone-aware datetime.
        """
        return self._dt

    def format(self, fmt: str) -> str:
        """Return formatted datetime as a string."""
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
    def _normalize_iso_format(cls, iso_str: str) -> str:
        """Normalize ISO 8601 string to be compatible with datetime.fromisoformat().

        Args:
            iso_str (str): Original ISO 8601 string.

        Returns:
            str: Normalized ISO 8601 string.
        """
        # Handle 'Z' suffix (Zulu time = UTC)
        if iso_str.endswith("Z"):
            iso_str = iso_str[:-1] + "+00:00"

        # Handle offset formats without colon (e.g., +0000, -0500)

        # Match timezone offset patterns like +HHMM or -HHMM at the end
        offset_pattern = r"([+-])(\d{2})(\d{2})$"
        match = re.search(offset_pattern, iso_str)
        if match:
            sign, hours, minutes = match.groups()
            # Replace with colon format
            iso_str = re.sub(offset_pattern, f"{sign}{hours}:{minutes}", iso_str)

        return iso_str

    @classmethod
    def _create_date_with_timezone_info(cls, dt: datetime) -> "Date":
        """Create a Date instance preserving timezone info from a datetime.

        Args:
            dt: A timezone-aware datetime object

        Returns:
            Date: A Date instance with preserved timezone
        """
        tz_name = cls._get_timezone_name(dt)

        # Create Date with the original datetime (preserving timezone)
        date_instance = cls.__new__(cls)
        date_instance._dt = dt

        # Create appropriate zone object
        has_tzinfo = dt.tzinfo is not None
        has_tzname = has_tzinfo and hasattr(dt.tzinfo, "tzname")
        has_key = has_tzinfo and hasattr(dt.tzinfo, "key")

        if has_tzinfo and has_tzname and not has_key:
            # For fixed offsets, store the timezone name
            date_instance._zone = type(
                "FixedOffset",
                (),
                {"key": tz_name, "tzname": lambda self, dt: tz_name},
            )()

        else:
            date_instance._zone = ZoneInfo(tz_name)

        return date_instance

    @classmethod
    def _get_timezone_name(cls, dt: datetime) -> str:
        """Get timezone name from a datetime object.

        Args:
            dt: A timezone-aware datetime object

        Returns:
            str: Timezone name
        """
        if dt.tzinfo is None:
            return "UTC"  # Default fallback for naive datetime

        if hasattr(dt.tzinfo, "key"):
            # ZoneInfo object
            return dt.tzinfo.key

        if dt.tzinfo == timezone.utc:
            # UTC timezone
            return "UTC"

        # Fixed offset timezone - use a generic name but preserve the offset
        return cls._format_offset_timezone_name(dt)

    @classmethod
    def _format_offset_timezone_name(cls, dt: datetime) -> str:
        """Format timezone name for fixed offset timezones.

        Args:
            dt: A timezone-aware datetime object with fixed offset

        Returns:
            str: Formatted timezone name like 'UTC+03:00'
        """
        if dt.tzinfo is None:
            return "UTC"  # Default fallback for naive datetime

        offset = dt.tzinfo.utcoffset(dt)
        if not offset:
            return "UTC"

        total_seconds = int(offset.total_seconds())
        hours, remainder = divmod(abs(total_seconds), 3600)
        minutes = remainder // 60
        sign = "+" if total_seconds >= 0 else "-"

        if minutes == 0:
            return f"UTC{sign}{hours:02d}"

        return f"UTC{sign}{hours:02d}:{minutes:02d}"

    @classmethod
    def from_timezone_aware_datetime(cls, dt: datetime) -> "Date":
        """Create a Date from a timezone-aware datetime, preserving the timezone.

        This is an internal method to handle timezone-aware datetimes without
        accessing protected members directly.

        Args:
            dt: A timezone-aware datetime object

        Returns:
            Date: A Date instance preserving the original timezone
        """
        if dt.tzinfo is None:
            raise ValueError("datetime must be timezone-aware")

        # For ZoneInfo objects, we can use the normal constructor
        if hasattr(dt.tzinfo, "key"):
            return cls(dt, tz=dt.tzinfo.key, naive="raise")

        # For UTC timezone
        if dt.tzinfo == timezone.utc:
            return cls(dt, tz="UTC", naive="raise")

        # For fixed offset timezones, we need special handling
        # Create the instance using __new__ and set attributes directly
        # This is the only case where we need to access protected members
        date_instance = cls.__new__(cls)
        date_instance._dt = dt

        # Create a timezone name for the offset
        offset = dt.tzinfo.utcoffset(dt)
        if offset:
            total_seconds = int(offset.total_seconds())
            hours, remainder = divmod(abs(total_seconds), 3600)
            minutes = remainder // 60
            sign = "+" if total_seconds >= 0 else "-"
            if minutes == 0:
                tz_name = f"UTC{sign}{hours:02d}"

            else:
                tz_name = f"UTC{sign}{hours:02d}:{minutes:02d}"

        else:
            tz_name = "UTC"

        # Create a mock zone object for fixed offsets
        date_instance._zone = type(
            "FixedOffset",
            (),
            {"key": tz_name, "tzname": lambda self, dt: tz_name},
        )()

        return date_instance

    @classmethod
    def from_iso(cls, iso_str: str, tz: Optional[str] = "UTC") -> Date:
        """Create a Date from an ISO 8601 string."""
        if tz is None:
            tz = "UTC"

        try:
            # Optimization: Try native parsing first (fastest for Py 3.11+)
            # Fast Path: UTC optimization using string concat (+00:00).
            # Avoids expensive .replace(tzinfo=...) calls.
            # Conds: tz="UTC", no '+', no 'Z', max 2 '-' (no negative offset)
            if (
                tz == "UTC"
                and "Z" not in iso_str
                and "+" not in iso_str
                and iso_str.count("-") <= 2
            ):
                try:
                    # Date-only (YYYY-MM-DD): Must append T00:00:00+00:00
                    # to force timezone awareness (otherwise naive).
                    if len(iso_str) == 10:
                        dt = datetime.fromisoformat(iso_str + "T00:00:00+00:00")

                    else:
                        # Timestamps: Appending +00:00 is sufficient.
                        dt = datetime.fromisoformat(iso_str + "+00:00")

                    # Success: We have a timezone-aware UTC datetime.
                    # Bypass constructor validation.
                    inst = cls.__new__(cls)
                    inst._dt = dt
                    inst._zone = _UTC_ZONE
                    return inst

                except ValueError:
                    # Fallback to standard flow if the concatenation trick failed
                    pass

            dt = datetime.fromisoformat(iso_str)

        except ValueError:
            try:
                # Fallback: Normalize the ISO string (legacy/edge cases)
                normalized_iso = cls._normalize_iso_format(iso_str)
                dt = datetime.fromisoformat(normalized_iso)

            except ValueError as exc:
                raise InvalidFormatError(
                    f"Date string '{iso_str}' is not a valid ISO 8601 format"
                ) from exc

        if dt.tzinfo is None:
            if tz == "UTC":
                # Fast Path: Constructor Bypass
                # We know dt is valid and we have the zone. Skip __init__ validation.
                inst = cls.__new__(cls)
                inst._dt = dt.replace(tzinfo=_UTC_ZONE)
                inst._zone = _UTC_ZONE
                return inst

            try:
                # Fast Path: Constructor Bypass for custom TZ
                inst = cls.__new__(cls)
                zone = ZoneInfo(tz)
                inst._dt = dt.replace(tzinfo=zone)
                inst._zone = zone
                return inst

            except ZoneInfoNotFoundError as exc:
                raise InvalidTimezoneError(tz) from exc

        # Timezone info present in ISO string, preserve it
        return cls._create_date_with_timezone_info(dt)

    @classmethod
    def from_unix(cls, timestamp: float, tz: Optional[str] = "UTC") -> Date:
        """Create a Date from a Unix timestamp.

        Args:
            timestamp (float): Seconds since epoch.
            tz (str, optional): Timezone. Defaults to "UTC".

        Returns:
            Date: Parsed Date.
        """
        if tz is None:
            tz = "UTC"

        try:
            dt = datetime.fromtimestamp(timestamp, tz=ZoneInfo(tz))

        except ZoneInfoNotFoundError as exc:
            raise InvalidTimezoneError(tz) from exc

        return cls(dt, tz)

    def is_within(self, other: Date, check_month: bool = True) -> bool:
        """Check if the current date is within the same
        year/month as another Date.

        Args:
            other (Date): Date to compare.
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

    def is_same_week(self, other: Date) -> bool:
        """Check if two dates fall in the same ISO calendar week.

        Args:
            other (Date): Date to compare.

        Returns:
            bool: True if both dates share the same ISO week.
        """
        return self._dt.isocalendar()[:2] == other.to_datetime().isocalendar()[:2]

    def is_same_day(self, other: Date) -> bool:
        """Return True if both dates fall on the same calendar day."""
        return self.to_datetime().date() == other.to_datetime().date()

    def is_before(self, other: Date) -> bool:
        """Return True if the current date is before ``other``."""
        return self.as_utc() < other.as_utc()

    def is_after(self, other: Date) -> bool:
        """Return True if the current date is after ``other``."""
        return self.as_utc() > other.as_utc()

    def is_leap_year(self) -> bool:
        """Return True if the current year is a leap year.

        Returns:
            bool: True if the year is a leap year, False otherwise.
        """
        year = self._dt.year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def is_weekend(self) -> bool:
        """Return True if the current date falls on a weekend (Saturday or Sunday).

        Returns:
            bool: True if the date is Saturday (5) or Sunday (6), False otherwise.
        """
        return is_weekend_day(self._dt.weekday())

    def is_monday(self) -> bool:
        """Return True if the current date is a Monday.

        Returns:
            bool: True if the date is Monday, False otherwise.
        """
        return self._dt.weekday() == 0

    def is_tuesday(self) -> bool:
        """Return True if the current date is a Tuesday.

        Returns:
            bool: True if the date is Tuesday, False otherwise.
        """
        return self._dt.weekday() == 1

    def is_wednesday(self) -> bool:
        """Return True if the current date is a Wednesday.

        Returns:
            bool: True if the date is Wednesday, False otherwise.
        """
        return self._dt.weekday() == 2

    def is_thursday(self) -> bool:
        """Return True if the current date is a Thursday.

        Returns:
            bool: True if the date is Thursday, False otherwise.
        """
        return self._dt.weekday() == 3

    def is_friday(self) -> bool:
        """Return True if the current date is a Friday.

        Returns:
            bool: True if the date is Friday, False otherwise.
        """
        return self._dt.weekday() == 4

    def is_saturday(self) -> bool:
        """Return True if the current date is a Saturday.

        Returns:
            bool: True if the date is Saturday, False otherwise.
        """
        return self._dt.weekday() == 5

    def is_sunday(self) -> bool:
        """Return True if the current date is a Sunday.

        Returns:
            bool: True if the date is Sunday, False otherwise.
        """
        return self._dt.weekday() == 6

    def days_until(self, other: Date) -> int:
        """Return the number of days until ``other``.

        Positive if ``other`` is later; negative if earlier.
        """
        delta = other.as_utc() - self.as_utc()
        return delta.days

    def as_utc(self) -> datetime:
        """Convert to UTC timezone.

        Returns:
            datetime: Datetime in UTC.
        """
        return self._dt.astimezone(timezone.utc)

    @property
    def as_local(self) -> datetime:
        """Return the datetime converted to the system's local timezone."""
        return self._dt.astimezone()

    def as_zone(self, zone: str) -> datetime:
        """Convert to a specific timezone.

        Args:
            zone (str): Target timezone name.

        Returns:
            datetime: Datetime in the new timezone.
        """
        try:
            return self._dt.astimezone(ZoneInfo(zone))

        except ZoneInfoNotFoundError as exc:
            raise InvalidTimezoneError(zone) from exc

    def truncate(self, unit: str) -> Date:
        """Truncate the Date to the specified unit (e.g., 'day', 'hour', etc.)."""
        valid_units = {"second", "minute", "hour", "day"}
        if unit not in valid_units:
            raise ValueError(
                f"Unsupported truncate unit '{unit}'. Valid units: {valid_units}"
            )

        # Cast to the expected Literal type for floor method
        unit_literal = cast(
            Literal["year", "month", "week", "day", "hour", "minute", "second"], unit
        )
        return self.floor(unit_literal)

    def replace(
        self,
        tz: Optional[str] = None,
        naive: Optional[Literal["utc", "local", "raise"]] = None,
        **kwargs: Any,
    ) -> Date:
        """Return a new Date with specific fields replaced."""
        filtered = {k: v for k, v in kwargs.items() if k in VALID_KEYS}
        new_dt = self._dt.replace(**filtered)
        return Date(new_dt, tz=tz or self._zone.key, naive=naive or "raise")

    def diff(
        self, other: Date, unit: Literal["days", "weeks", "months", "years"] = "days"
    ) -> int:
        """Return the absolute difference in the specified unit."""
        if unit == "days":
            return abs((self._dt - other.to_datetime()).days)

        if unit == "weeks":
            return abs((self._dt - other.to_datetime()).days) // 7

        if unit == "months":
            return abs(self.month_span_to(other))

        if unit == "years":
            return abs(self.year_span_to(other))

        raise ValueError("Unsupported unit. Use 'days', 'weeks', 'months', 'years'.")

    def diff_for_humans(
        self, other: Optional["Date"] = None, locale: str = "en"
    ) -> str:
        """Return a human-readable difference between two dates."""
        if other is not None and not isinstance(other, Date):
            raise TypeError("'other' must be a Date instance")

        return _diff_for_humans(self, other, locale)

    def next_weekday(self, weekday: int) -> Date:
        """Return the next date matching the specified weekday.

        Args:
            weekday (int): Target weekday (0 = Monday).

        Returns:
            Date: The next date matching the weekday.
        """
        current_weekday = self._dt.weekday()
        days_ahead = (weekday - current_weekday + 7) % 7 or 7
        next_date = self._dt + timedelta(days=days_ahead)
        return Date(next_date, self._zone.key)

    def previous_weekday(self, weekday: int) -> Date:
        """Return the previous date matching the specified weekday.

        Args:
            weekday (int): Target weekday (0 = Monday).

        Returns:
            Date: The previous date matching the weekday.
        """
        current_weekday = self._dt.weekday()
        days_behind = (current_weekday - weekday + 7) % 7 or 7
        prev_date = self._dt - timedelta(days=days_behind)
        return Date(prev_date, self._zone.key)

    def floor(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> Date:
        """Return a new Date aligned to the start of the given unit."""
        truncate_map = {
            "year": {
                "month": 1,
                "day": 1,
                "hour": 0,
                "minute": 0,
                "second": 0,
                "microsecond": 0,
            },
            "month": {
                "day": 1,
                "hour": 0,
                "minute": 0,
                "second": 0,
                "microsecond": 0,
            },
            "week": {"hour": 0, "minute": 0, "second": 0, "microsecond": 0},
            "day": {"hour": 0, "minute": 0, "second": 0, "microsecond": 0},
            "hour": {"minute": 0, "second": 0, "microsecond": 0},
            "minute": {"second": 0, "microsecond": 0},
            "second": {"microsecond": 0},
        }

        if unit not in truncate_map:
            raise ValueError(f"Unsupported unit: {unit}")

        dt = self._dt
        if unit == "week":
            dt -= timedelta(days=dt.weekday())

        replace_kwargs = cast(dict, truncate_map[unit])
        return self._with(dt.replace(**replace_kwargs))

    def ceil(self, unit: str) -> Date:
        """
        Returns a new Date advanced to the end of the given unit.
        """
        # Cast to the expected Literal type for floor method
        unit_literal = cast(
            Literal["year", "month", "week", "day", "hour", "minute", "second"], unit
        )
        floored = self.floor(unit_literal).to_datetime()

        if unit == "year":
            dt = floored.replace(
                month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
            )

        elif unit == "month":
            last_day = monthrange(floored.year, floored.month)[1]
            dt = floored.replace(
                day=last_day, hour=23, minute=59, second=59, microsecond=999999
            )

        elif unit == "week":
            dt = floored + timedelta(days=6)
            dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)

        elif unit == "day":
            dt = floored.replace(hour=23, minute=59, second=59, microsecond=999999)

        elif unit == "hour":
            dt = floored.replace(minute=59, second=59, microsecond=999999)

        elif unit == "minute":
            dt = floored.replace(second=59, microsecond=999999)

        elif unit == "second":
            dt = floored.replace(microsecond=999999)

        else:
            raise ValueError(f"Unsupported unit: {unit}")

        return self._with(dt)

    def start_of(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> Date:
        """
        Returns the datetime aligned to the start of the given unit.

        Args:
            unit (Literal): Temporal unit.

        Returns:
            Date: Aligned datetime.
        """
        return self.floor(unit)

    def end_of(
        self, unit: Literal["year", "month", "week", "day", "hour", "minute", "second"]
    ) -> Date:
        """
        Returns the datetime aligned to the end of the given unit.

        Args:
            unit (Literal): Temporal unit.

        Returns:
            Date: Aligned datetime.
        """
        return self.ceil(unit)

    def month_span_to(self, other: Date) -> int:
        """
        Return the number of full calendar months between self and other.
        Positive if `other` is later. Negative if `other` is earlier.
        """
        d1 = self.to_datetime()
        d2 = other.to_datetime()

        if d1 > d2:
            d1, d2 = d2, d1
            sign = -1

        else:
            sign = 1

        years_diff = d2.year - d1.year
        months_diff = d2.month - d1.month
        total_months = years_diff * 12 + months_diff

        if d2.day < d1.day:
            total_months -= 1

        return sign * total_months

    def year_span_to(self, other: Date) -> int:
        """
        Return the number of full calendar years between self and other.
        Positive if `other` is later. Negative if `other` is earlier.

        Example:
            Date("2020-05-20").year_span_to(Date("2024-05-19")) == 3
            Date("2020-05-20").year_span_to(Date("2024-05-20")) == 4
        """
        d1, d2 = sorted([self.to_datetime(), other.to_datetime()])
        span = d2.year - d1.year
        if (d2.month, d2.day) < (d1.month, d1.day):
            span -= 1

        return span if self._dt <= other.to_datetime() else -span

    def to_dict(self) -> dict:
        """Return a dictionary representation of the Date."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "second": self.second,
            "microsecond": self.microsecond,
            "timezone": self._zone.key,
        }

    def start_of_day(self) -> "Date":
        """Return a new Date instance representing the start of the current day."""
        return self._with(self._dt.replace(hour=0, minute=0, second=0, microsecond=0))

    def end_of_day(self) -> "Date":
        """Return a new Date instance representing the end of the current day."""
        return self._with(
            self._dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        )

    def start_of_month(self) -> "Date":
        """Return a new Date instance for the first moment of the current month."""
        return self._with(
            self._dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        )

    def end_of_month(self) -> "Date":
        """
        Return a new Date instance representing the last moment of the current month
        (23:59:59.999999 UTC).
        """
        year = self._dt.year
        month = self._dt.month

        # Calcular el primer día del mes siguiente
        if month == 12:
            next_month = datetime(year + 1, 1, 1, tzinfo=self._dt.tzinfo)

        else:
            next_month = datetime(year, month + 1, 1, tzinfo=self._dt.tzinfo)

        # Restar un microsegundo para obtener el último instante del mes actual
        next_month_date = self._with(next_month)
        return cast("Date", next_month_date - timedelta(microseconds=1))

    def start_of_year(self) -> "Date":
        """Return a new Date instance for the first moment of the current year."""
        return self._with(
            self._dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        )

    def end_of_year(self) -> "Date":
        """Return a Date for the last moment of the current year."""
        next_year = datetime(self._dt.year + 1, 1, 1, tzinfo=self._dt.tzinfo)
        next_year_date = self._with(next_year)
        return cast("Date", next_year_date - timedelta(microseconds=1))
