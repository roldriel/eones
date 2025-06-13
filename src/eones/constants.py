"""contants.py"""

# Default date formats (ISO and common human-readable)
DEFAULT_FORMATS = [
    "%Y-%m-%d",  # 2025-06-15
    "%d/%m/%Y",  # 15/06/2025
    "%Y/%m/%d",  # 2025/06/15
    "%d-%m-%Y",  # 15-06-2025
    "%d.%m.%Y",  # 15.06.2025
    "%Y-%m-%d %H:%M:%S",  # 2025-06-15 13:45:00
    "%d/%m/%Y %H:%M:%S",  # 15/06/2025 13:45:00
    "%Y-%m-%dT%H:%M:%S",  # 2025-06-15T13:45:00 (ISO sin tz)
    "%Y-%m-%dT%H:%M",  # 2025-06-15T13:45
    "%Y-%m-%d %H:%M",  # 2025-06-15 13:45
    "%d %b %Y",  # 15 Jun 2025
    "%d %B %Y",  # 15 June 2025
    "%Y%m%d",  # 20250615
    "%d%m%Y",  # 15062025
    "%Y-%m-%dT%H:%M:%S.%f",  # 2025-06-15T13:45:00.000
    "%Y-%m-%dT%H:%M:%S.%fZ",  # 2025-06-15T13:45:00.000Z
    "%a %b %d %H:%M:%S %Y",  # Mon Jun 15 13:45:00 2025
]

# Default timezone
DEFAULT_TIMEZONE = "UTC"

# Valid keys for datetime dictionary parsing
VALID_KEYS = {"year", "month", "day", "hour", "minute", "second", "microsecond"}

# Valid fields for delta specification
DELTA_KEYS = {"years", "months", "weeks", "days", "hours", "minutes", "seconds"}
