# Common Use Cases with Eones

This file contains practical examples of using Eones in real-world situations.

## 1. Calculate Age

```python
birth_date = Eones("1990-05-15")
today = Eones()

age = today.difference(birth_date, unit="years")
print(f"Age: {age.total_months // 12} years")
```

## 2. Due Dates

```python
today = Eones()
due_date = Eones(today)
due_date.add(days=30)  # Due in 30 days

print(f"Due on: {due_date.format('%d/%m/%Y')}")
print(f"Time remaining: {due_date.diff_for_humans(locale='en')}")
```

## 3. Monthly Reports

```python
report_date = Eones("2024-06-15")

# Get the complete month range
month_start, month_end = report_date.range("month")

print(f"Monthly report: {month_start.strftime('%B %Y')}")
print(f"From: {month_start.strftime('%d/%m/%Y')}")
print(f"To: {month_end.strftime('%d/%m/%Y')}")
```

## 4. Work Schedules

```python
# Find next Monday for a meeting
today = Eones()
next_monday = today.next_weekday(0)  # 0 = Monday

# Set meeting time
meeting = Eones(next_monday)
meeting.replace(hour=9, minute=0)  # 9:00 AM

print(f"Next meeting: {meeting.format('%A %B %d at %H:%M')}")
```

## 5. Invoice Validation

```python
# Case 1: Validate if an invoice is within the current month
invoice_date = Eones("2025-06-08")
current = Eones("2025-06-15")
if current.is_within(invoice_date):
    print("The invoice corresponds to the current month")
```

## 6. Calculate Remaining Days

```python
# Case 2: Calculate how many days until expiration
expiration = Eones("2025-06-20")
today = Eones("2025-06-15")
remaining_days = today.difference(expiration, unit="days")
print("Days until expiration:", remaining_days)
```

## 7. Fiscal Quarter Detection

```python
# Case 3: Detect if a date is the start of a fiscal quarter
date = Eones("2025-07-01")
if date.format("%m-%d") in ["01-01", "04-01", "07-01", "10-01"]:
    print("Start of fiscal quarter")
```

## 8. Period Report

```python
# Case 4: Generate a report from the beginning of the month to today
today = Eones("2025-06-18")
month_start, _ = today.range("month")
print("Report from:", month_start.date(), "to", today.now().to_datetime().date())
```

## 9. Next Cutoff Date

```python
# Case 5: Estimate next weekly cutoff date (Monday)
today = Eones("2025-06-18")
cutoff = today.next_weekday(0)
print("Next Monday:", cutoff.to_datetime().strftime("%Y-%m-%d"))
```

## 10. Work Calendar

```python
# List of holidays (can come from an external database)
holidays = [
    "2025-01-01",  # New Year
    "2025-05-01",  # Labor Day
    "2025-12-25",  # Christmas
]

# Check if a date is a working day
date = Eones("2025-05-01")

is_weekend = date.now().to_datetime().weekday() >= 5  # 5 = Saturday, 6 = Sunday
is_holiday = date.format("%Y-%m-%d") in holidays

if is_weekend or is_holiday:
    print("Non-working day")
else:
    print("Working day")
```

## 11. Calculate Next Working Days

```python
# Calculate next 5 working days
current = Eones("2025-05-01")
next_days = []

while len(next_days) < 5:
    current.add(days=1)
    dt = current.now().to_datetime()
    if dt.weekday() < 5 and current.format("%Y-%m-%d") not in holidays:
        next_days.append(current.format("%Y-%m-%d"))

print("Next 5 working days:", next_days)
```

## 12. API Formatting

```python
# Serialization for REST APIs
def date_for_api(date):
    return {
        "date": format_date(date, "%Y-%m-%d"),
        "readable_date": format_date(date, "%B %d, %Y"),
        "timestamp": date.timestamp()
    }
```

## 13. Database Storage

```python
# Database storage
def save_event(name, date, duration):
    return {
        "name": name,
        "iso_date": format_date(date, "%Y-%m-%dT%H:%M:%S%z"),
        "iso_duration": format_duration(duration)
    }
```

## 14. Structured Logs

```python
import logging

# Structured logs
def log_event(event, date):
    logging.info(f"Event '{event}' scheduled for {format_date(date, '%Y-%m-%d %H:%M')}")
```