# Celery Integration

Eones objects can be passed to Celery tasks by converting them to ISO 8601 strings before sending and parsing them back inside the task.

## Serialization Pattern

Celery serializes task arguments using JSON by default. Since `Eones` and `Date` are not natively JSON-serializable, convert them at the boundary:

```python
from celery import Celery
from eones import Eones

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def send_reminder(date_iso: str, message: str):
    scheduled = Eones(date_iso)
    print(f"Reminder for {scheduled.format('%Y-%m-%d')}: {message}")

# Enqueue the task
due = Eones("2025-06-15T09:00:00+00:00")
send_reminder.delay(due.for_json(), "Team standup")
```

## Custom Celery Serializer

For transparent serialization, register a custom JSON serializer that uses `eones_encoder`:

```python
import json
from kombu.serialization import register
from eones.integrations.serializers import eones_encoder

def eones_dumps(obj):
    return json.dumps(obj, default=eones_encoder)

def eones_loads(s):
    return json.loads(s)

register(
    "eones-json",
    eones_dumps,
    eones_loads,
    content_type="application/json",
    content_encoding="utf-8",
)

# Configure Celery to use it
app.conf.update(
    accept_content=["eones-json", "json"],
    task_serializer="eones-json",
    result_serializer="eones-json",
)
```

With this configuration, Eones objects in task arguments and return values are serialized automatically. Note that deserialization still returns strings &mdash; wrap them with `Eones()` inside the task.

## Periodic Tasks with Eones

Use Eones to calculate dynamic schedules:

```python
from eones import Eones

now = Eones()
next_monday = now.next_weekday(0)
eta = next_monday.to_datetime()

send_reminder.apply_async(
    args=[now.for_json(), "Weekly report"],
    eta=eta,
)
```
