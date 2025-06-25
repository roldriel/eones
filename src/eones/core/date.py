"""core.date.py"""

from __future__ import annotations

from calendar import monthrange
from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Optional, Union
from zoneinfo import ZoneInfo

from eones.constants import VALID_KEYS
from eones.humanize import diff_for_humans as _diff_for_humans


class Date:  # pylint: disable=too-many-public-methods
    """
    Encapsulates a precise moment in time, drawn from the infinite thread of eons.

    This class offers a rich set of operations for navigating,
    formatting, and comparing temporal instances, while remaining rooted
    in timezone-aware datetime logic.  It bridges raw timekeeping with
    semantic clarity, allowing you to reason about durations, truncations,
    alignments, and transitions in a way that feels both practical and timeless.
    """

    def __init__(
        self,
        dt: Optional[datetime] = None,
        tz: Optional[str] = "UTC",
        naive: Literal["utc", "local", "raise"] = "raise",
    ):
        self._zone = ZoneInfo(tz)

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

    def __add__(self, delta: timedelta) -> Date:
        return self.shift(delta)

    def __sub__(self, other: Union[Date, timedelta]) -> Union[Date, timedelta]:
        if isinstance(other, timedelta):
            return self.shift(-other)

        if isinstance(other, Date):
            return self._dt - other.to_datetime()
        return NotImplemented

    @classmethod
    def now(
        cls, tz: str = "UTC", naive: Literal["utc", "local", "raise"] = "raise"
    ) -> Date:
        """
        Create a Date for the current moment.

        Args:
            tz (str): Timezone to apply.
            naive (str): How to interpret if the datetime is naive. Accepts
                "utc", "local", or "raise". Only meaningful if tz is applied
                after generation.

        Returns:
            Date: Instance representing now.
        """
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
    def from_iso(cls, iso_str: str, tz: Optional[str] = "UTC") -> Date:
        """Create a Date from an ISO 8601 string.

        Args:
            iso_str (str): ISO date string.
            tz (str, optional): Timezone. Defaults to "UTC".

        Returns:
            Date: Parsed Date.
        """
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo(tz))
        return cls(dt, tz)

    @classmethod
    def from_unix(cls, timestamp: float, tz: Optional[str] = "UTC") -> Date:
        """Create a Date from a Unix timestamp.

        Args:
            timestamp (float): Seconds since epoch.
            tz (str, optional): Timezone. Defaults to "UTC".

        Returns:
            Date: Parsed Date.
        """
        dt = datetime.fromtimestamp(timestamp, tz=ZoneInfo(tz))
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
        return self._dt.astimezone(ZoneInfo(zone))

    def truncate(self, unit: str) -> Date:
        """Truncate the Date to the specified unit (e.g., 'day', 'hour', etc.)."""
        valid_units = {"second", "minute", "hour", "day"}
        if unit not in valid_units:
            raise ValueError(
                f"Unsupported truncate unit '{unit}'. Valid units: {valid_units}"
            )
        return self.floor(unit)

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
        return self._with(dt.replace(**truncate_map[unit]))

    def ceil(self, unit: str) -> Date:
        """
        Returns a new Date advanced to the end of the given unit.
        """
        floored = self.floor(unit).to_datetime()

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
        last_instant = next_month - timedelta(microseconds=1)
        return self._with(last_instant)

    def start_of_year(self) -> "Date":
        """Return a new Date instance for the first moment of the current year."""
        return self._with(
            self._dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        )

    def end_of_year(self) -> "Date":
        """Return a Date for the last moment of the current year."""
        next_year = datetime(self._dt.year + 1, 1, 1, tzinfo=self._dt.tzinfo)
        last_instant = next_year - timedelta(microseconds=1)
        return self._with(last_instant)
