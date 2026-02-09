# 🛠️ Advanced Date Manipulation

## Truncation and Rounding

```python
from eones import Eones
date = Eones("2024-06-15 14:30:45")

# Truncate to the start of different units
date.floor("day")     # Eones(date=2024-06-15T00:00:00+00:00, tz='UTC')
date.floor("month")   # Eones(date=2024-06-01T00:00:00+00:00, tz='UTC')

# Advance to the end of different units
date.ceil("day")      # Eones(date=2024-01-01T23:59:59.999999+00:00, tz='UTC')

# Round to the nearest unit
date.round("day")     # Round to the nearest day
```

## Start and End of Periods

```python
date = Eones("2024-06-15 14:30:45")

# Go to the start of different periods
date.start_of("day")     # 2024-06-15 00:00:00
date.start_of("week")    # Monday of that week

# Go to the end of different periods
date.end_of("month")     # 2024-06-30 23:59:59
```

## Component Replacement

```python
date = Eones("2024-06-15 14:30:45")

# Change specific components
date.replace(day=1)           # Change to day 1 of the month
date.replace(hour=0, minute=0, second=0)  # Midnight
```
