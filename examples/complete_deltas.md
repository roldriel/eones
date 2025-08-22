# Working with Deltas in Eones

Eones implements a sophisticated delta system with **dual architecture** that clearly separates time intervals into two categories.

## Dual Delta Architecture

1. **`DeltaCalendar`**: For calendar-based intervals (years, months, days)
2. **`DeltaDuration`**: For absolute duration-based intervals (days, hours, minutes, seconds)

## Main `Delta` Class

The main `Delta` class acts as a facade that combines both types:

```python
from eones.delta import Delta

# Deltas are automatically created when calculating differences
date1 = Eones("2024-01-01")
date2 = Eones("2024-03-15")

delta = date2.difference(date1)
print(delta)  # Shows the difference in readable format

# Deltas can be applied to dates
new_date = date1.add(months=2, days=14)  # Equivalent to the previous delta
```

### Main Methods of `Delta`

```python
# Create deltas
delta = Delta(years=1, months=2, days=10, hours=5, minutes=30)

# From standard timedelta
from datetime import timedelta
td = timedelta(days=3, seconds=3600)
delta = Delta.from_timedelta(td)

# From ISO 8601 format
delta = Delta.from_iso("P1Y2M10DT3H30M")
print(delta.to_iso())  # "P1Y2M10DT3H30M"

# Conversions
print(delta.total_seconds())  # Duration components only
print(delta.total_months())   # 12 * years + months

# Operations
delta1 = Delta(days=5)
delta2 = Delta(days=2)
result = delta1 - delta2  # Delta(days=3)
```

## `DeltaCalendar` - Calendar Intervals

Handles intervals that depend on calendar structure (years, months, days):

```python
from eones.core.delta_calendar import DeltaCalendar
from eones.date import Date

# Create calendar delta
dc = DeltaCalendar(years=1, months=2, days=10)

# Apply to a date (automatically handles month boundaries)
d = Date(2024, 1, 31)  # January 31st
new_date = dc.apply(d)  # Add 1 month
print(new_date.to_string())  # "2024-02-29" (handles leap year)

# Special end-of-month cases
end_of_month = Date(2024, 1, 31)
one_month = DeltaCalendar(months=1)
result = one_month.apply(end_of_month)
print(result.to_string())  # "2024-02-29" (not "2024-02-31")

# Invert delta
negative_dc = dc.invert()
print(negative_dc.years, negative_dc.months)  # -1, -2

# Operations
dc1 = DeltaCalendar(months=3)
dc2 = DeltaCalendar(months=1)
result = dc1 - dc2  # DeltaCalendar(months=2)
```

## `DeltaDuration` - Duration Intervals

Handles absolute time intervals that don't depend on the calendar:

```python
from eones.core.delta_duration import DeltaDuration
from eones.date import Date

# Create duration delta
dd = DeltaDuration(days=2, hours=3, minutes=30, seconds=45)

# Apply to a date
d = Date.from_string("2024-06-15T10:00:00")
new_date = dd.apply(d)
print(new_date.to_string("%Y-%m-%d %H:%M:%S"))  # "2024-06-17 13:30:45"

# Convert to standard timedelta
td = dd.to_timedelta()
print(td)  # "2 days, 3:30:45"

# Invert delta
negative_dd = dd.invert()
print(negative_dd.hours)  # -3

# Operations
dd1 = DeltaDuration(hours=5)
dd2 = DeltaDuration(hours=2)
result = dd1 - dd2  # DeltaDuration(hours=3)
```

## When to Use Each Type

**Use `DeltaCalendar` when:**
- Working with months and years ("next month", "in 2 years")
- Need to respect calendar boundaries (end of month, leap years)
- Performing due date or anniversary calculations

**Use `DeltaDuration` when:**
- Working with precise time intervals ("in 2 hours and 30 minutes")
- Need absolute duration independent of calendar
- Performing elapsed time or timeout calculations

**Use main `Delta` when:**
- Need to combine both types of intervals
- Want the simplest and most complete interface
- Working with automatically calculated differences

## Practical Examples

### Monthly Due Date

```python
# Monthly due date (uses DeltaCalendar)
due_date = Date(2024, 1, 31)
next_due = DeltaCalendar(months=1).apply(due_date)
print(next_due)  # 2024-02-29 (not 2024-02-31)
```

### Session Timeout

```python
# Session timeout (uses DeltaDuration)
session_start = Date.now()
timeout = DeltaDuration(hours=2)
session_expires = timeout.apply(session_start)
print(f"Session expires: {session_expires.format('%H:%M')}")
```

### Complex Reminder

```python
# Complex reminder (uses combined Delta)
reminder = Delta(months=1, hours=2)  # One month and 2 hours later
reminder_date = reminder.apply(Date.now())
```