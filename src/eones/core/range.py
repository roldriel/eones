"""core.range.py"""

from __future__ import annotations

from calendar import monthrange
from datetime import datetime, time, timedelta
from typing import Tuple

from eones.core.date import Date


class Range:
    """
    Generates the start and end bounds of a temporal window.

    Based on a given Date, this class exposes methods to calculate the exact
    datetime boundaries of days, months, and years — including edge-aligned timestamps
    suitable for querying, slicing, and framing temporal datasets.
    """

    def __init__(self, date: Date):
        """Initialize the range object with a base Date.

        Args:
            date (Date): The reference date for range generation.
        """
        self.date = date

    def __repr__(self) -> str:
        """Return a string representation of the Range instance.

        Returns:
            str: Debug-friendly string showing the reference date.
        """
        return f"Range(date={repr(self.date)})"

    def day_range(self) -> Tuple[datetime, datetime]:
        """Return the start and end of the current day.

        Returns:
            Tuple[datetime, datetime]: Start and end of the day.
        """
        dt = self.date.to_datetime()
        start = datetime.combine(dt.date(), time.min).replace(tzinfo=dt.tzinfo)
        end = datetime.combine(dt.date(), time.max).replace(tzinfo=dt.tzinfo)
        return start, end

    def month_range(self) -> Tuple[datetime, datetime]:
        """Return the start and end of the current month.

        Returns:
            Tuple[datetime, datetime]: Start and end of the month.
        """
        dt = self.date.to_datetime()
        _, last_day = monthrange(dt.year, dt.month)
        start = datetime(dt.year, dt.month, 1, 0, 0, 0, tzinfo=dt.tzinfo)
        end = datetime(
            dt.year, dt.month, last_day, 23, 59, 59, 999999, tzinfo=dt.tzinfo
        )
        return start, end

    def year_range(self) -> Tuple[datetime, datetime]:
        """Return the start and end of the current year.

        Returns:
            Tuple[datetime, datetime]: Start and end of the year.
        """
        dt = self.date.to_datetime()
        start = datetime(dt.year, 1, 1, 0, 0, 0, tzinfo=dt.tzinfo)
        end = datetime(dt.year, 12, 31, 23, 59, 59, 999999, tzinfo=dt.tzinfo)
        return start, end

    def week_range(self) -> Tuple[datetime, datetime]:
        """Return the start (Monday) and end (Sunday) of the current ISO week.

        Returns:
            Tuple[datetime, datetime]: Start and end of the week.
        """
        dt = self.date.to_datetime()
        start_date = dt - timedelta(days=dt.weekday())
        start = datetime.combine(start_date.date(), time.min).replace(tzinfo=dt.tzinfo)
        end_date = start_date + timedelta(days=6)
        end = datetime.combine(end_date.date(), time.max).replace(tzinfo=dt.tzinfo)
        return start, end

    def quarter_range(self) -> Tuple[datetime, datetime]:
        """Return the start and end of the current quarter.

        Returns:
            Tuple[datetime, datetime]: Start and end of the quarter.
        """
        dt = self.date.to_datetime()
        quarter = (dt.month - 1) // 3
        start_month = quarter * 3 + 1
        end_month = start_month + 2
        start = datetime(dt.year, start_month, 1, 0, 0, 0, tzinfo=dt.tzinfo)
        _, last_day = monthrange(dt.year, end_month)
        end = datetime(
            dt.year, end_month, last_day, 23, 59, 59, 999999, tzinfo=dt.tzinfo
        )
        return start, end

    def custom_range(
        self, start_delta: "Delta", end_delta: "Delta"
    ) -> Tuple[datetime, datetime]:
        """Return a range defined by applying deltas to the base date.

        Args:
            start_delta (Delta): Delta applied to generate the start.
            end_delta (Delta): Delta applied to generate the end.

        Returns:
            Tuple[datetime, datetime]: Resulting start and end datetimes.
        """
        from eones.core.delta import Delta  # local import to avoid circular

        if not isinstance(start_delta, Delta) or not isinstance(end_delta, Delta):
            raise TypeError("start_delta and end_delta must be Delta instances")

        start_dt = start_delta.apply(self.date).to_datetime()
        end_dt = end_delta.apply(self.date).to_datetime()
        if start_dt > end_dt:
            start_dt, end_dt = end_dt, start_dt
        return start_dt, end_dt
