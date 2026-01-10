# 🛡️ Error Handling

Eones defines a robust system of specific exceptions for different types of errors, all inheriting from a common base class `EonesError`.

## Exception Hierarchy

```python
from eones.errors import (
    EonesError,                    # Base exception
    InvalidTimezoneError,          # Invalid timezone
    InvalidDateFormatError,        # Invalid date format
    InvalidDurationFormatError     # Invalid duration format
)
```

## `EonesError` - Base Exception

All custom Eones exceptions inherit from this base class:

```python
class EonesError(Exception):
    pass
```

This allows catching any Eones-specific error:

```python
try:
    date = Eones("invalid-date", tz="Nonexistent/Zone")
except EonesError as e:
    print(f"Eones error: {e}")
```

## `InvalidTimezoneError`

Raised when an unrecognized timezone is provided:

```python
try:
    date = Eones("2024-01-01", tz="Nonexistent/Zone")
except InvalidTimezoneError as e:
    print(f"Invalid timezone: {e}")
    # Use default timezone
    date = Eones("2024-01-01")  # UTC by default
```

## `InvalidDateFormatError`

Raised when the date string cannot be parsed correctly:

```python
try:
    date = Eones("completely-invalid-date")
except InvalidDateFormatError as e:
    print(f"Invalid date format: {e}")
    # Try with specific format
    date = Eones("2024-01-01", formats=["%Y-%m-%d"])
```

## `InvalidDurationFormatError`

Raised when an ISO 8601 duration string is invalid:

```python
from eones.delta import Delta

try:
    delta = Delta.from_iso("P1Y2M3D4H5M6S-INVALID")
except InvalidDurationFormatError as e:
    print(f"Invalid ISO duration format: {e}")
    # Create delta manually
    delta = Delta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
```

## Robust Error Handling

### Safe Creation Function

```python
def create_safe_date(date_str, tz_str=None):
    """Creates a date safely with error handling."""
    try:
        return Eones(date_str, tz=tz_str)
    except InvalidDateFormatError:
        print(f"Invalid date format: {date_str}")
        return None
    except InvalidTimezoneError:
        print(f"Invalid timezone: {tz_str}, using UTC")
        return Eones(date_str)  # UTC by default
    except EonesError as e:
        print(f"General Eones error: {e}")
        return None

# Usage
date = create_safe_date("2024-12-25", "Europe/Madrid")
if date:
    print(f"Date created: {date.format('%Y-%m-%d %Z')}")
```

### Multiple Format Handling

```python
def parse_flexible_date(date_str):
    """Attempts to parse a date with multiple strategies."""
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for format_str in formats:
        try:
            return Eones(date_str, formats=[format_str])
        except InvalidDateFormatError:
            continue
    
    # If no format works
    raise InvalidDateFormatError(f"Could not parse date: {date_str}")

# Usage
try:
    date = parse_flexible_date("25/12/2024")
    print(f"Parsed date: {date.format('%Y-%m-%d')}")
except InvalidDateFormatError as e:
    print(f"Error: {e}")
```

### User Input Validation

```python
def validate_user_input(date_input, tz_input=None):
    """Validates and processes user input with detailed feedback."""
    errors = []
    
    # Validate date
    date = None
    try:
        date = Eones(date_input, tz=tz_input)
    except InvalidDateFormatError:
        errors.append(f"Invalid date format: '{date_input}'")
        errors.append("Valid formats: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY")
    except InvalidTimezoneError:
        errors.append(f"Invalid timezone: '{tz_input}'")
        errors.append("Valid timezone example: 'Europe/Madrid', 'America/New_York'")
        # Try without timezone
        try:
            date = Eones(date_input)
            errors.append("Using UTC as default timezone")
        except InvalidDateFormatError:
            errors.append("Could not parse date without timezone either")
    except EonesError as e:
        errors.append(f"Unexpected error: {e}")
    
    return date, errors

# Usage
date, errors = validate_user_input("25/12/2024", "Europe/Madrid")
if errors:
    for error in errors:
        print(f"⚠️  {error}")
if date:
    print(f"✅ Valid date: {date.format('%Y-%m-%d %Z')}")
```

### Error Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_date_with_logging(date_str, tz_str=None):
    """Processes date with detailed error logging."""
    try:
        date = Eones(date_str, tz=tz_str)
        logger.info(f"Date processed successfully: {date.format('%Y-%m-%d %Z')}")
        return date
    except InvalidDateFormatError as e:
        logger.error(f"Date format error: {e}")
        logger.info(f"Input received: '{date_str}'")
        raise
    except InvalidTimezoneError as e:
        logger.warning(f"Invalid timezone: {e}")
        logger.info(f"Retrying with UTC...")
        return Eones(date_str)  # Fallback to UTC
    except EonesError as e:
        logger.error(f"Unexpected Eones error: {e}")
        raise
```

## Exception Usage Contexts

These exceptions are used internally in:
- **`parser.py`**: When parsing invalid dates or durations
- **`Date` and `Delta`**: When initializing objects with incorrect data
- **`interface.py`**: When validating user inputs
- **Conversion methods**: When converting between formats

## Best Practices

1. **Always catch specific exceptions** before the base exception
2. **Provide helpful error messages** to the user
3. **Implement sensible fallbacks** when possible
4. **Log errors** for debugging and monitoring
5. **Validate inputs** before processing when critical