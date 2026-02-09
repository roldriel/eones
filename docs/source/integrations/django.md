# Django Integration

Eones provides a built-in `DateTimeField` that transparently converts between `Date` objects and `datetime` values stored in Django models.

## Model Field

```python
from django.db import models
from eones.integrations.django import DateTimeField

class Event(models.Model):
    name = models.CharField(max_length=200)
    starts_at = DateTimeField()
    ends_at = DateTimeField(null=True, blank=True)
```

### Writing to the database

Assign `Date` objects directly to the field. They are converted to `datetime` before storage:

```python
from eones.core.date import Date

event = Event.objects.create(
    name="Team meeting",
    starts_at=Date(),  # current UTC time
)
```

### Reading from the database

Values are automatically returned as `Date` instances:

```python
event = Event.objects.get(pk=1)
print(type(event.starts_at))  # <class 'eones.core.date.Date'>
print(event.starts_at.format("%Y-%m-%d %H:%M"))  # 2025-06-15 10:00
print(event.starts_at.is_weekend())  # True/False
```

### Form and validation support

The field supports `to_python()`, which means it works with Django forms and model validation. It accepts:

- `None` (for nullable fields)
- `Date` instances (passed through unchanged)
- `datetime` objects (converted to `Date`)
- ISO 8601 strings (parsed via Django's parent `DateTimeField`, then converted)

## API Reference

### `DateTimeField`

Extends `django.db.models.DateTimeField`.

- **`from_db_value(value, expression, connection)`**: Converts a `datetime` from the database to a `Date` instance. Returns `None` for `NULL` values.
- **`to_python(value)`**: Converts strings, datetimes, or `Date` objects for form/validation use.
- **`get_prep_value(value)`**: Converts a `Date` to `datetime` for database storage.
