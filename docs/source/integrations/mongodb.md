# MongoDB Integration

Eones works with MongoDB (via PyMongo or Motor) by converting `Date` and `Eones` objects to `datetime` before storage and wrapping them back on retrieval.

## Basic Pattern with PyMongo

MongoDB stores dates as BSON `datetime`. Convert at the boundary:

```python
from datetime import datetime, timezone
from pymongo import MongoClient
from eones import Eones

client = MongoClient("mongodb://localhost:27017")
db = client["myapp"]

# Store
event_date = Eones("2025-06-15T09:00:00+00:00")
db.events.insert_one({
    "name": "Team standup",
    "scheduled_at": event_date.to_datetime(),
})

# Retrieve
doc = db.events.find_one({"name": "Team standup"})
scheduled = Eones(doc["scheduled_at"])
print(scheduled.format("%Y-%m-%d %H:%M"))  # "2025-06-15 09:00"
```

## Helper Functions

Centralise the conversion logic so it stays consistent across your codebase:

```python
from eones import Eones
from eones.core.date import Date

def to_mongo(value):
    """Convert an Eones or Date object to a datetime for MongoDB."""
    if isinstance(value, (Eones, Date)):
        return value.to_datetime()
    return value

def from_mongo(value):
    """Convert a MongoDB datetime back to an Eones object."""
    if value is None:
        return None
    return Eones(value)
```

Usage:

```python
# Insert
db.events.insert_one({
    "name": "Deploy",
    "created_at": to_mongo(Eones()),
})

# Query
doc = db.events.find_one({"name": "Deploy"})
created = from_mongo(doc["created_at"])
```

## Querying by Date Range

```python
from eones import Eones

start = Eones("2025-06-01")
end = Eones("2025-06-30")

results = db.events.find({
    "scheduled_at": {
        "$gte": start.to_datetime(),
        "$lte": end.to_datetime(),
    }
})

for doc in results:
    print(from_mongo(doc["scheduled_at"]).format("%d/%m/%Y"))
```

## Async with Motor

The same pattern applies when using Motor (async MongoDB driver):

```python
import motor.motor_asyncio
from eones import Eones

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["myapp"]

async def create_event(name: str, date: Eones):
    await db.events.insert_one({
        "name": name,
        "scheduled_at": date.to_datetime(),
    })

async def get_event(name: str) -> dict:
    doc = await db.events.find_one({"name": name})
    if doc:
        doc["scheduled_at"] = Eones(doc["scheduled_at"])
    return doc
```

## Timezone Considerations

MongoDB stores `datetime` in UTC. If your Eones objects carry a specific timezone, the offset is applied during `to_datetime()` and the resulting UTC value is what gets stored. On retrieval, wrap with `Eones()` and convert to the desired timezone:

```python
from eones import Eones

# Store a date with timezone
madrid = Eones("2025-06-15T14:00:00", tz="Europe/Madrid")
db.events.insert_one({"date": madrid.to_datetime()})  # stored as UTC

# Retrieve and convert back
doc = db.events.find_one()
utc_date = Eones(doc["date"])
local_date = utc_date.to_timezone("Europe/Madrid")
print(local_date)  # 2025-06-15T14:00:00+02:00
```
