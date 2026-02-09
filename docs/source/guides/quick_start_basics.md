# ⚡ Quick Start

This section covers the basics of using the Eones library.

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
