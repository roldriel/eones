# ⚖️ Comparisons and Validations

## Date Comparisons

```python
from eones import Eones
date1 = Eones("2024-01-01")
date2 = Eones("2024-12-31")
date3 = Eones("2024-06-15")

# Check if a date is between two others
is_between = date3.is_between(date1, date2)
print(is_between)  # True

# Check if they are in the same week
same_week = date1.is_same_week(date2)
```

## Next Weekdays

```python
date = Eones("2024-06-15")  # Assume it's Saturday

# Find the next Monday (0=Monday, 6=Sunday)
next_monday = date.next_weekday(0)

# Find the previous specific weekday
previous_wednesday = date.previous_weekday(2)
```
