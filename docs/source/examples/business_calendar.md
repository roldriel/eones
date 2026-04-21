# Business Days & Holiday Calendars

Eones provides built-in holiday calendars for 7 countries and a full suite of business day operations. Calendars and locale are orthogonal concepts — you can combine any locale with any calendar.

## Available Calendars

```python
from eones import Eones

Eones.available_calendars()
# ['America/Argentina', 'America/US', 'Asia/Japan',
#  'Europe/France', 'Europe/Germany', 'Europe/Spain',
#  'Oceania/Australia']
```

## Setting a Calendar

### Via constructor (recommended)

```python
# Calendar is inherited by all subsequent method calls
e = Eones("2026-05-25", calendar="America/Argentina")
e.is_holiday()      # True (Dia de la Revolucion de Mayo)
e.is_business_day()  # False
```

### Per-call override

```python
e = Eones("2026-07-04")
e.is_holiday(calendar="America/US")        # True (Independence Day)
e.is_holiday(calendar="Europe/France")     # False
```

## Checking Holidays

```python
e = Eones("2026-12-25", calendar="Europe/Germany")

e.is_holiday()    # True
e.holiday_name()  # "1. Weihnachtstag"

# Non-holiday
e2 = Eones("2026-06-15", calendar="Europe/Germany")
e2.is_holiday()    # False
e2.holiday_name()  # None
```

## Navigating Business Days

```python
e = Eones("2026-05-01", calendar="Europe/France")

# Next/previous business day
e.next_business_day()      # 2026-05-04 (skips weekend + Fete du Travail)
e.previous_business_day()  # 2026-04-30

# Add/subtract business days
e.add_business_days(5)       # Skips weekends and holidays
e.subtract_business_days(3)  # Goes back 3 working days
```

## Counting Business Days

```python
# Static methods — no instance needed
Eones.count_business_days("2026-01-01", "2026-01-31", calendar="America/US")
Eones.count_weekends("2026-01-01", "2026-01-31")
Eones.count_holidays("2026-01-01", "2026-12-31", calendar="Asia/Japan")
```

## Time Until Weekend / Business Day

```python
e = Eones("2026-03-11", calendar="America/Argentina")  # Wednesday

e.time_until_weekend()       # 3 (days until Saturday)
e.time_until_business_day()  # 0 (already a business day)

# On a weekend
sat = Eones("2026-03-14", calendar="America/Argentina")
sat.time_until_business_day()  # 2 (Monday)
```

## Custom Weekend Configuration

Some regions observe different weekends. Pass a `FrozenSet[int]` where 0=Monday, 6=Sunday:

```python
# Friday-Saturday weekend (common in Middle East)
e = Eones("2026-06-07")  # Sunday
e.is_business_day(weekend=frozenset({4, 5}))  # True (Sunday is a workday)
```

## Registering a Custom Calendar

```python
from eones.calendars import HolidayCalendar, register_calendar
from eones.core.date import Date

class MyCompanyCalendar(HolidayCalendar):
    def holidays(self, year):
        return [
            Date(year, 1, 1),   # New Year
            Date(year, 12, 25), # Christmas
            Date(year, 8, 15),  # Company Foundation Day
        ]

    def holiday_name(self, date):
        names = {
            (1, 1): "New Year",
            (12, 25): "Christmas",
            (8, 15): "Company Foundation Day",
        }
        key = (date.month, date.day)
        return names.get(key)

register_calendar("Custom/MyCompany", MyCompanyCalendar)

e = Eones("2026-08-15", calendar="Custom/MyCompany")
e.is_holiday()    # True
e.holiday_name()  # "Company Foundation Day"
```

## Multi-Country Example

```python
# Compare business days across countries for the same date range
start, end = "2026-01-01", "2026-12-31"

for cal in ["America/Argentina", "America/US", "Asia/Japan", "Oceania/Australia"]:
    bdays = Eones.count_business_days(start, end, calendar=cal)
    holidays = Eones.count_holidays(start, end, calendar=cal)
    print(f"{cal}: {bdays} business days, {holidays} holidays")
```

## Combining Calendar and Locale

Calendar (holidays) and locale (language) are independent:

```python
# Argentine holidays, Japanese output
e = Eones("2026-05-25", locale="ja", calendar="America/Argentina")
e.is_holiday()                  # True
e.diff_for_humans("2026-05-20") # "5 日前"

# Japanese holidays, Spanish output
e = Eones("2026-04-29", locale="es", calendar="Asia/Japan")
e.is_holiday()                  # True (Showa no Hi)
e.diff_for_humans("2026-04-26") # "hace 3 dias"
```
