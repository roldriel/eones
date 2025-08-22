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