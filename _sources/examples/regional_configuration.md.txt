# 🌍 Regional Configuration

Eones v1.4.0 introduces the ability to configure the first day of the week to adapt to different cultural and regional standards.

## Global Configuration

By default, Eones uses the ISO standard where Monday is the first day of the week (value 0). You can change this by modifying the `FIRST_DAY_OF_WEEK` constant:

```python
from eones import constants

# Configure for ISO standard (Monday first) - default
constants.FIRST_DAY_OF_WEEK = 0

# Configure for US standard (Sunday first)
constants.FIRST_DAY_OF_WEEK = 6
```

## Impact on Methods

### is_weekend()

The `is_weekend()` method automatically adapts to the configuration:

```python
from eones import Date
from eones import constants
from datetime import datetime

# Create a Friday date
friday = Date(datetime(2024, 1, 5))  # Friday

# ISO Standard (Monday first): Friday is NOT a weekend
constants.FIRST_DAY_OF_WEEK = 0
print(f"ISO - Friday is weekend: {friday.is_weekend()}")  # False

# US Standard (Sunday first): Friday IS a weekend
constants.FIRST_DAY_OF_WEEK = 6
print(f"US - Friday is weekend: {friday.is_weekend()}")   # True
```

### week_range()

The `week_range()` method also accepts an optional parameter to specify the first day:

```python
from eones import Date, Range
from datetime import datetime

# Tuesday, June 10, 2025
date = Date(datetime(2025, 6, 10))
r = Range(date)

# ISO Week (Monday to Sunday)
start_iso, end_iso = r.week_range(first_day_of_week=0)
print(f"ISO Week: {start_iso.day} to {end_iso.day}")  # 9 to 15

# US Week (Sunday to Saturday)
start_us, end_us = r.week_range(first_day_of_week=6)
print(f"US Week: {start_us.day} to {end_us.day}")    # 8 to 14
```

## Helper Functions

Eones provides helper functions to convert between numbering systems:

```python
from eones.constants import iso_to_us_weekday, us_to_iso_weekday, is_weekend_day

# Convert from ISO to US
iso_monday = 0  # Monday in ISO
us_monday = iso_to_us_weekday(iso_monday)
print(f"ISO Monday ({iso_monday}) = US Monday ({us_monday})")  # 0 = 1

# Convert from US to ISO
us_sunday = 0  # Sunday in US
iso_sunday = us_to_iso_weekday(us_sunday)
print(f"US Sunday ({us_sunday}) = ISO Sunday ({iso_sunday})")  # 0 = 6

# Check weekend with specific configuration
print(f"Is Friday a weekend in ISO? {is_weekend_day(4, 0)}")  # False
print(f"Is Friday a weekend in US? {is_weekend_day(4, 6)}")   # True
```

## Numbering Systems

### ISO (International Standard)
- 0: Monday
- 1: Tuesday
- 2: Wednesday
- 3: Thursday
- 4: Friday
- 5: Saturday
- 6: Sunday
- **Weekend**: Saturday and Sunday

### US (United States Standard)
- 0: Sunday
- 1: Monday
- 2: Tuesday
- 3: Wednesday
- 4: Thursday
- 5: Friday
- 6: Saturday
- **Weekend**: Friday and Saturday (in ISO numbering: 4 and 5)

## Use Cases

### International Applications
```python
# Configure based on user region
def configure_week_by_region(region):
    if region in ['US', 'CA', 'MX']:  # North America
        constants.FIRST_DAY_OF_WEEK = 6  # Sunday first
    else:  # Europe, Asia, etc.
        constants.FIRST_DAY_OF_WEEK = 0  # Monday first
```

### Business Reports
```python
# Generate weekly report adapted to local culture
def generate_weekly_report(date, region='ISO'):
    r = Range(date)
    first_day = 6 if region == 'US' else 0
    start, end = r.week_range(first_day_of_week=first_day)
    
    print(f"Weekly report from {start.strftime('%d/%m/%Y')} to {end.strftime('%d/%m/%Y')}")
    return start, end
```

## Important Notes

1. **Compatibility**: Changing `FIRST_DAY_OF_WEEK` globally affects all methods that depend on week configuration.

2. **Persistence**: The configuration persists throughout the Python session. For permanent changes, consider configuring it at the start of your application.

3. **Thread Safety**: Be careful when changing configuration in multi-threaded applications, as it affects globally.

4. **Backward Compatibility**: By default, Eones maintains existing ISO behavior, so existing code will continue to work without changes.