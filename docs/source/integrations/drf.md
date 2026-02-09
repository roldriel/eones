# Django REST Framework Integration

Eones works with DRF by creating a custom serializer field that converts between `Date` objects and ISO 8601 strings.

## Custom Serializer Field

```python
from rest_framework import serializers
from eones.core.date import Date

class EonesDateField(serializers.Field):
    """DRF field that serializes/deserializes Eones Date objects."""

    def to_representation(self, value):
        if isinstance(value, Date):
            return value.to_iso()
        return str(value)

    def to_internal_value(self, data):
        try:
            return Date.from_iso(data)
        except Exception as exc:
            raise serializers.ValidationError(
                f"Invalid date format: {data}"
            ) from exc
```

## Usage in Serializers

```python
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    starts_at = EonesDateField()
    ends_at = EonesDateField(required=False, allow_null=True)
```

### Serialization (output)

```python
from eones.core.date import Date

event = {"name": "Meeting", "starts_at": Date()}
serializer = EventSerializer(event)
serializer.data
# {"name": "Meeting", "starts_at": "2025-06-15T10:00:00+00:00"}
```

### Deserialization (input)

```python
data = {"name": "Meeting", "starts_at": "2025-06-15T10:00:00+00:00"}
serializer = EventSerializer(data=data)
serializer.is_valid(raise_exception=True)
print(type(serializer.validated_data["starts_at"]))  # <class 'eones.core.date.Date'>
```

## With ModelSerializer

If your Django model uses `eones.integrations.django.DateTimeField`, map it to `EonesDateField` in the serializer:

```python
class EventModelSerializer(serializers.ModelSerializer):
    starts_at = EonesDateField()

    class Meta:
        model = Event
        fields = ["id", "name", "starts_at"]
```
