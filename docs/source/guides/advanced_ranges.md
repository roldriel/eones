# 📏 Date Ranges

## Range Iteration

```python
from eones import Eones
from datetime import timedelta

start = Eones("2023-01-01")
end = Eones("2023-01-05")

# Iterate with a specific step
for date in Eones.range_iter(start, end, timedelta(days=1)):
    print(date.format("%Y-%m-%d"))
```

## Period Ranges

```python
date = Eones("2024-06-15")

# Get specific ranges
quarter_range = date.quarter_range()  # Start and end of current quarter
iso_week_range = date.week_range()    # ISO week (Monday to Sunday)
```
