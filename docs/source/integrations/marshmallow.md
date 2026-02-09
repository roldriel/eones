# Marshmallow Integration

Eones works with marshmallow by creating a custom field that serializes `Date` objects to ISO 8601 strings and deserializes them back.

## Custom Field

```python
from marshmallow import fields, ValidationError
from eones.core.date import Date

class EonesDateField(fields.Field):
    """Marshmallow field for Eones Date objects."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, Date):
            return value.to_iso()
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return Date.from_iso(value)
        except Exception as exc:
            raise ValidationError(
                f"Invalid date format: {value}"
            ) from exc
```

## Usage in Schemas

```python
from marshmallow import Schema

class EventSchema(Schema):
    name = fields.String(required=True)
    starts_at = EonesDateField(required=True)
    ends_at = EonesDateField(load_default=None)
```

### Serialization (dump)

```python
from eones.core.date import Date

event = {"name": "Meeting", "starts_at": Date(), "ends_at": None}
schema = EventSchema()
result = schema.dump(event)
# {"name": "Meeting", "starts_at": "2025-06-15T10:00:00+00:00", "ends_at": null}
```

### Deserialization (load)

```python
data = {"name": "Meeting", "starts_at": "2025-06-15T10:00:00+00:00"}
schema = EventSchema()
result = schema.load(data)
print(type(result["starts_at"]))  # <class 'eones.core.date.Date'>
```

### Validation errors

```python
data = {"name": "Meeting", "starts_at": "not-a-date"}
schema = EventSchema()
errors = schema.validate(data)
# {"starts_at": ["Invalid date format: not-a-date"]}
```
