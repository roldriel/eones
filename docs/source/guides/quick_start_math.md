# ➕ Math & Diff

## Adding and Subtracting Time

```python
from eones import Eones
date = Eones("2024-01-15")

# Add time
date.add(days=10)              # Eones(date=2024-01-25T00:00:00+00:00, tz='UTC')
date.add(months=2)             # Eones(date=2024-03-25T00:00:00+00:00, tz='UTC')
date.add(years=1, days=5)      # Eones(date=2025-03-30T00:00:00+00:00, tz='UTC')
date.add(hours=3, minutes=30)  # Eones(date=2025-03-30T03:30:00+00:00, tz='UTC')

print(date.format("%Y-%m-%d %H:%M"))  # 2025-03-30 03:30
```

## Calculate differences

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

# Human-readable difference
print(date2.diff_for_humans(date1))  # in 1 year
print(date2.diff_for_humans(date1, locale="es"))  # en 1 año
```
