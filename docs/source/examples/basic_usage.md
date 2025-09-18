# Basic Usage of Eones

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

# From Python datetime
from datetime import datetime
date6 = Eones(datetime.now())

# From ISO 8601 strings (with timezone support)
date7 = Eones("2024-12-25T15:30:00Z")           # UTC
date8 = Eones("2024-12-25T15:30:00+03:00")      # With positive offset
date9 = Eones("2024-12-25T15:30:00-05:00")      # With negative offset
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
print(date.format("%Y-%m-%d"))           # 2024-12-25
print(date.format("%d/%m/%Y"))           # 25/12/2024
print(date.format("%d de %B de %Y"))     # 25 de December de 2024
print(date.format("%H:%M:%S"))           # 15:30:00
```

## Adding and Subtracting Time

### Adding time to a date

```python
date = Eones("2024-01-15")

# Add time
date.add(days=10)          # Add 10 days
date.add(months=2)         # Add 2 months
date.add(years=1, days=5)  # Add 1 year and 5 days
date.add(hours=3, minutes=30)  # Add 3 hours and 30 minutes

print(date.format("%Y-%m-%d %H:%M"))  # Result after additions
```

## Differences Between Dates

### Calculate differences

```python
date1 = Eones("2024-01-01")
date2 = Eones("2024-12-31")

# Calculate difference
difference = date2.difference(date1)
print(difference)  # Shows the difference in Delta format

# Difference in specific units
days_difference = date2.difference(date1, unit="days")
months_difference = date2.difference(date1, unit="months")

# Human-readable difference
print(date2.diff_for_humans(date1))  # "11 months ago" (in English)
print(date2.diff_for_humans(date1, locale="es"))  # "hace 11 meses" (in Spanish)
```

## Custom Parsing

### Using custom formats

```python
# Use custom formats
custom_formats = ["%d-%m-%Y", "%Y/%m/%d"]
date = Eones("15-06-2024", formats=custom_formats)

# Add additional formats to defaults
date = Eones("15-06-2024", additional_formats=["%d-%m-%Y"])
```

## Localization

### Support for multiple languages

```python
date1 = Eones("2024-01-01")
date2 = Eones("2024-01-15")

# In English (default)
print(date2.diff_for_humans(date1))  # "2 weeks ago"

# In Spanish
print(date2.diff_for_humans(date1, locale="es"))  # "hace 2 semanas"
```