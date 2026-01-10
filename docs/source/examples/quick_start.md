# ⚡ Quick Start

This file contains basic examples to get started with the Eones library.

## Import

```python
from eones import Eones
```

## Creating Dates

### Different ways to create dates

```python
# Current date
current_date = Eones()

# From string (multiple formats supported)
date1 = Eones("2024-12-25")
date2 = Eones("25/12/2024")
date3 = Eones("25-12-2024")
date4 = Eones("2024-12-25 15:30:00")

# From dictionary
date5 = Eones({"year": 2024, "month": 12, "day": 25, "hour": 15})

# From Python datetime (must be timezone-aware)
from datetime import datetime, timezone
date6 = Eones(datetime.now(timezone.utc))

# From ISO 8601 strings (with timezone support)
date7 = Eones("2024-12-25T15:30:00Z")               # UTC
date8 = Eones("2024-12-25T15:30:00+03:00")          # With positive offset
date9 = Eones("2024-12-25T15:30:00-05:00")          # With negative offset
date10 = Eones("2024-12-25T15:30:00.123456+02:30")  # With microseconds and offset

# With specific timezone
madrid_date = Eones("2024-12-25", tz="Europe/Madrid")
mexico_date = Eones("2024-12-25", tz="America/Mexico_City")
```

## Date Formatting

### Different output formats

```python
date = Eones("2024-12-25 15:30:00")

# Different output formats
print(date.format("%Y-%m-%d"))  # 2024-12-25
print(date.format("%d/%m/%Y"))  # 25/12/2024
print(date.format("%d %B %Y"))  # 25 December 2024
print(date.format("%H:%M:%S"))  # 15:30:00
```

## Adding and Subtracting Time

### Adding time to a date

```python
date = Eones("2024-01-15")

# Add time
date.add(days=10)              # Eones(date=2024-01-25T00:00:00+00:00, tz='UTC')
date.add(months=2)             # Eones(date=2024-03-25T00:00:00+00:00, tz='UTC')
date.add(years=1, days=5)      # Eones(date=2025-03-30T00:00:00+00:00, tz='UTC')
date.add(hours=3, minutes=30)  # Eones(date=2025-03-30T03:30:00+00:00, tz='UTC')

print(date.format("%Y-%m-%d %H:%M"))  # 2025-03-30 03:30
```

## Differences Between Dates

### Calculate differences

```python
date1 = Eones("2024-01-01")
date2 = Eones("2024-12-31")

# Calculate difference
difference = date2.difference(date1)
print(difference)  # 365

# Difference in specific units
days_difference = date2.difference(date1, unit="days")
months_difference = date2.difference(date1, unit="months")
years_difference = date2.difference(date1, unit="years")
print(days_difference)    # 365
print(months_difference)  # 11
print(years_difference)   # 0

# Human-readable difference
print(date2.diff_for_humans(date1))  # in 1 year
print(date2.diff_for_humans(date1, locale="es"))  # en 1 año
```

## Custom Parsing

### Using custom formats

```python
# Use custom formats
custom_formats = ["%d-%m-%Y", "%Y/%m/%d"]
date = Eones("15-06-2024", formats=custom_formats)
print(date)  # Eones(date=2024-06-15T00:00:00+00:00, tz='UTC')

# Add additional formats to defaults
date = Eones("15-06-2024", additional_formats=["%d-%m-%Y"])
print(date)  # Eones(date=2024-06-15T00:00:00+00:00, tz='UTC')
```

## Localization

### Support for multiple languages

```python
date1 = Eones("2024-01-01")
date2 = Eones("2024-01-15")

# In English (default)
print(date2.diff_for_humans(date1))  # in 2 weeks

# In Spanish
print(date2.diff_for_humans(date1, locale="es"))  # en 2 semanas
```
