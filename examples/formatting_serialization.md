# Advanced Formatting and Serialization in Eones

Eones includes specialized utilities for formatting and serialization of `Date` and `Delta` objects.

## Date Formatting

### Basic Formatting

```python
from eones.formats import format_date
from eones.date import Date

# Basic formatting
d = Date(2024, 6, 15)
print(format_date(d))  # "2024-06-15" (default format)
print(format_date(d, "%d/%m/%Y"))  # "15/06/2024"
```

### Formatting with Timezone

```python
# Formatting with timezone
d_madrid = Date(2024, 6, 15, tz="Europe/Madrid")
print(format_date(d_madrid, "%Y-%m-%d %H:%M %Z"))  # "2024-06-15 00:00 CEST"

# Used internally by Date.to_string()
print(d.to_string("%A, %B %d, %Y"))  # Uses format_date internally
```

## Duration Serialization

### ISO 8601 Serialization

```python
from eones.formats import format_duration
from eones.delta import Delta

# ISO 8601 serialization
delta = Delta(years=1, months=2, days=3, hours=4, minutes=30)
print(format_duration(delta))  # "P1Y2M3DT4H30M"
```

### Special Duration Cases

```python
# Special cases
delta_time_only = Delta(hours=2, minutes=15)
print(format_duration(delta_time_only))  # "PT2H15M"

delta_date_only = Delta(years=1, days=10)
print(format_duration(delta_date_only))  # "P1Y10D"

# Used internally by Delta.to_iso()
print(delta.to_iso())  # Uses format_duration internally
```

## Common Use Cases

### Serialization for REST APIs

```python
def date_for_api(date):
    """Converts a date for use in REST APIs."""
    return {
        "date": format_date(date, "%Y-%m-%d"),
        "readable_date": format_date(date, "%B %d, %Y"),
        "timestamp": date.timestamp()
    }

# Usage example
date = Date(2024, 12, 25)
api_data = date_for_api(date)
print(api_data)
# {
#     "date": "2024-12-25",
#     "readable_date": "December 25, 2024",
#     "timestamp": 1735084800.0
# }
```

### Database Storage

```python
def save_event(name, date, duration):
    """Prepares event data for database storage."""
    return {
        "name": name,
        "date_iso": format_date(date, "%Y-%m-%dT%H:%M:%S%z"),
        "duration_iso": format_duration(duration)
    }

# Usage example
event_date = Date(2024, 6, 15, 14, 30)
event_duration = Delta(hours=2, minutes=30)

event_data = save_event("Team meeting", event_date, event_duration)
print(event_data)
# {
#     "name": "Team meeting",
#     "date_iso": "2024-06-15T14:30:00+00:00",
#     "duration_iso": "PT2H30M"
# }
```

### Structured Logging

```python
import logging

def log_event(event, date):
    """Logs an event with readable date format."""
    formatted_date = format_date(date, '%Y-%m-%d %H:%M')
    logging.info(f"Event '{event}' scheduled for {formatted_date}")

# Usage example
log_date = Date(2024, 6, 15, 10, 30)
log_event("Automatic backup", log_date)
# INFO:root:Event 'Automatic backup' scheduled for 2024-06-15 10:30
```

### JSON Export

```python
import json
from datetime import datetime

class EonesJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Eones objects."""
    
    def default(self, obj):
        if isinstance(obj, Date):
            return {
                "_type": "Date",
                "iso": format_date(obj, "%Y-%m-%dT%H:%M:%S%z"),
                "readable": format_date(obj, "%B %d, %Y at %H:%M")
            }
        elif isinstance(obj, Delta):
            return {
                "_type": "Delta",
                "iso": format_duration(obj),
                "components": {
                    "years": obj.years,
                    "months": obj.months,
                    "days": obj.days,
                    "hours": obj.hours,
                    "minutes": obj.minutes,
                    "seconds": obj.seconds
                }
            }
        return super().default(obj)

# Usage example
data = {
    "event": "Conference",
    "date": Date(2024, 9, 15, 9, 0),
    "duration": Delta(hours=8, minutes=30)
}

json_str = json.dumps(data, cls=EonesJSONEncoder, indent=2)
print(json_str)
```

### JSON Import

```python
def decode_eones_json(dct):
    """Decodes Eones objects from JSON."""
    if "_type" in dct:
        if dct["_type"] == "Date":
            return Date.from_string(dct["iso"])
        elif dct["_type"] == "Delta":
            return Delta.from_iso(dct["iso"])
    return dct

# Usage example
json_data = '''
{
  "event": "Conference",
  "date": {
    "_type": "Date",
    "iso": "2024-09-15T09:00:00+00:00"
  },
  "duration": {
    "_type": "Delta",
    "iso": "PT8H30M"
  }
}
'''

data = json.loads(json_data, object_hook=decode_eones_json)
print(f"Event: {data['event']}")
print(f"Date: {data['date'].format('%d/%m/%Y %H:%M')}")
print(f"Duration: {data['duration'].total_seconds() / 3600} hours")
```

### Locale-Specific Formatting

```python
def format_date_locale(date, locale="en"):
    """Formats date according to specified locale."""
    formats = {
        "es": "%d de %B de %Y",
        "en": "%B %d, %Y",
        "fr": "%d %B %Y",
        "de": "%d. %B %Y"
    }
    
    format_str = formats.get(locale, formats["en"])
    return format_date(date, format_str)

# Usage example
date = Date(2024, 6, 15)
print(format_date_locale(date, "es"))  # "15 de June de 2024"
print(format_date_locale(date, "en"))  # "June 15, 2024"
print(format_date_locale(date, "fr"))  # "15 June 2024"
```

### Format Validation

```python
def validate_date_format(date_str, format_str):
    """Validates if a date string matches the expected format."""
    try:
        date = Date.from_string(date_str)
        formatted_date = format_date(date, format_str)
        return date_str == formatted_date
    except Exception:
        return False

# Usage example
print(validate_date_format("2024-06-15", "%Y-%m-%d"))  # True
print(validate_date_format("15/06/2024", "%Y-%m-%d"))  # False
```

## ISO 8601 Parsing with Timezone Offsets

Eones provides comprehensive support for parsing ISO 8601 formatted strings with timezone offsets, both through the `Date.from_iso()` method and the `Parser` class.

### Using Date.from_iso()

```python
from eones import Date

# Basic ISO 8601 with UTC
date1 = Date.from_iso("2024-01-15T10:30:00Z")
print(date1)  # 2024-01-15T10:30:00+00:00

# ISO 8601 with positive offset
date2 = Date.from_iso("2024-01-15T10:30:00+03:00")
print(date2)  # 2024-01-15T10:30:00+03:00
print(date2.timezone)  # UTC+03:00

# ISO 8601 with negative offset
date3 = Date.from_iso("2024-01-15T10:30:00-05:00")
print(date3)  # 2024-01-15T10:30:00-05:00
print(date3.timezone)  # UTC-05:00

# ISO 8601 with microseconds and offset
date4 = Date.from_iso("2024-01-15T10:30:00.123456+02:30")
print(date4)  # 2024-01-15T10:30:00.123456+02:30
```

### Supported Offset Formats

```python
# Various offset formats are supported
formats = [
    "2024-01-15T10:30:00Z",           # UTC (Zulu time)
    "2024-01-15T10:30:00+00:00",      # UTC with explicit offset
    "2024-01-15T10:30:00+03:00",      # Positive offset with colon
    "2024-01-15T10:30:00-05:00",      # Negative offset with colon
    "2024-01-15T10:30:00+0300",       # Positive offset without colon
    "2024-01-15T10:30:00-0500",       # Negative offset without colon
    "2024-01-15T10:30:00.123+01:00",  # With milliseconds
    "2024-01-15T10:30:00.123456-02:00" # With microseconds
]

for fmt in formats:
    date = Date.from_iso(fmt)
    print(f"{fmt:<35} -> {date} (TZ: {date.timezone})")
```

### Using Parser with ISO 8601 Formats

```python
from eones import Parser

# Create a parser (default formats now include ISO 8601 with offsets)
parser = Parser()

# Parse various ISO 8601 formats
iso_strings = [
    "2024-01-15T10:30:00Z",
    "2024-01-15T10:30:00+03:00",
    "2024-01-15T10:30:00.123456-05:00"
]

for iso_str in iso_strings:
    date = parser.parse(iso_str)
    print(f"Parsed: {date} (Timezone: {date.timezone})")
```

### Custom Timezone for Naive ISO Strings

```python
# When parsing naive ISO strings, you can specify a default timezone
naive_iso = "2024-01-15T10:30:00"

# Using Date.from_iso() with custom timezone
date_ny = Date.from_iso(naive_iso, tz="America/New_York")
print(f"New York: {date_ny} (TZ: {date_ny.timezone})")

# Using Parser with custom default timezone
parser_tokyo = Parser(tz="Asia/Tokyo")
date_tokyo = parser_tokyo.parse(naive_iso)
print(f"Tokyo: {date_tokyo} (TZ: {date_tokyo.timezone})")
```

### Timezone Preservation

```python
# When an ISO string contains timezone information, it's preserved
# even if you specify a different default timezone

iso_with_offset = "2024-01-15T10:30:00+05:30"

# The +05:30 offset is preserved, not overridden by America/New_York
date = Date.from_iso(iso_with_offset, tz="America/New_York")
print(f"Original offset preserved: {date} (TZ: {date.timezone})")
# Output: 2024-01-15T10:30:00+05:30 (TZ: UTC+05:30)
```

### Error Handling for Invalid Offsets

```python
from eones.errors import InvalidFormatError

# Invalid offset formats will raise InvalidFormatError
invalid_formats = [
    "2024-01-15T10:30:00+25:00",  # Invalid hour offset
    "2024-01-15T10:30:00+03:70",  # Invalid minute offset
    "2024-01-15T10:30:00+abc",    # Non-numeric offset
]

for invalid_fmt in invalid_formats:
    try:
        date = Date.from_iso(invalid_fmt)
    except InvalidFormatError as e:
        print(f"Invalid format '{invalid_fmt}': {e}")
```