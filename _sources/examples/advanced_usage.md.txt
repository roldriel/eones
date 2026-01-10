# Advanced Usage of Eones

This file contains advanced examples of date and time manipulation with Eones.

## Advanced Date Manipulation

### Truncation and Rounding

```python
date = Eones("2024-06-15 14:30:45")

# Truncate to the start of different units
date.floor("day")     # 2024-06-15 00:00:00
date.floor("month")   # 2024-06-01 00:00:00
date.floor("year")    # 2024-01-01 00:00:00
date.floor("hour")    # 2024-06-15 14:00:00

# Advance to the end of different units
date.ceil("day")      # 2024-06-15 23:59:59
date.ceil("month")    # 2024-06-30 23:59:59
date.ceil("year")     # 2024-12-31 23:59:59

# Round to the nearest unit
date.round("hour")    # Round to the nearest hour
date.round("day")     # Round to the nearest day
```

### Start and End of Periods

```python
date = Eones("2024-06-15 14:30:45")

# Go to the start of different periods
date.start_of("day")     # 2024-06-15 00:00:00
date.start_of("week")    # Monday of that week
date.start_of("month")   # 2024-06-01 00:00:00
date.start_of("year")    # 2024-01-01 00:00:00

# Go to the end of different periods
date.end_of("day")       # 2024-06-15 23:59:59
date.end_of("week")      # Sunday of that week
date.end_of("month")     # 2024-06-30 23:59:59
date.end_of("year")      # 2024-12-31 23:59:59
```

### Component Replacement

```python
date = Eones("2024-06-15 14:30:45")

# Change specific components
date.replace(day=1)           # Change to day 1 of the month
date.replace(month=12)        # Change to December
date.replace(year=2025)       # Change to 2025
date.replace(hour=0, minute=0, second=0)  # Midnight

print(date.format("%Y-%m-%d %H:%M:%S"))
```

## Comparisons and Validations

### Date Comparisons

```python
date1 = Eones("2024-01-01")
date2 = Eones("2024-12-31")
date3 = Eones("2024-06-15")

# Check if a date is between two others
is_between = date3.is_between(date1, date2)
print(is_between)  # True

# Check if they are in the same week
same_week = date1.is_same_week(date2)
print(same_week)  # False

# Check if they are in the same month/year
same_month = date1.is_within(date3, check_month=True)
same_year = date1.is_within(date3, check_month=False)
```

### Next Weekdays

```python
date = Eones("2024-06-15")  # Assume it's Saturday

# Find the next Monday (0=Monday, 6=Sunday)
next_monday = date.next_weekday(0)
print(next_monday.format("%Y-%m-%d"))  # Date of next Monday

# Next Friday
next_friday = date.next_weekday(4)
print(next_friday.format("%Y-%m-%d"))
```

## Date Ranges

### Get period ranges

```python
date = Eones("2024-06-15")

# Get ranges for different periods
day_range = date.range("day")      # (day_start, day_end)
month_range = date.range("month")    # (month_start, month_end)
year_range = date.range("year")     # (year_start, year_end)

# Ranges return datetime tuples
start, end = month_range
print(f"Month: from {start} to {end}")
```

## Additional Methods of the Date Class

### Navigation by Weekdays

```python
date = Eones("2024-06-15")  # Assume it's Saturday

# Find the next specific weekday
next_monday = date.next_weekday(0)    # 0=Monday, 1=Tuesday, ..., 6=Sunday
next_friday = date.next_weekday(4)

# Find the previous specific weekday
previous_wednesday = date.previous_weekday(2)

print(next_monday.format("%Y-%m-%d"))     # Date of next Monday
print(previous_wednesday.format("%Y-%m-%d")) # Date of previous Wednesday
```

### Dictionary Conversion

```python
date = Eones("2024-06-15 14:30:45")

# Convert to dictionary with all components
date_dict = date.to_dict()
print(date_dict)
# {
#     'year': 2024,
#     'month': 6,
#     'day': 15,
#     'hour': 14,
#     'minute': 30,
#     'second': 45,
#     'microsecond': 0,
#     'timezone': 'UTC'
# }
```

### Specific Period Ranges

```python
date = Eones("2024-06-15")

# Get specific ranges using the Range class
quarter_range = date.quarter_range()  # Start and end of current quarter
iso_week_range = date.week_range()    # ISO week (Monday to Sunday)

# Ranges return datetime tuples
quarter_start, quarter_end = quarter_range
print(f"Quarter: {quarter_start} - {quarter_end}")
```