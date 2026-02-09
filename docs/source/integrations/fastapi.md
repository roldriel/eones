# FastAPI & Pydantic Integration

Eones works with FastAPI and Pydantic using custom validators and the built-in `eones_encoder` for JSON serialization.

## Custom Pydantic Type

To use `Eones` or `Date` as a Pydantic field, define an annotated type with a `BeforeValidator`:

```python
from typing import Annotated
from pydantic import BaseModel, BeforeValidator
from eones import Eones

def validate_eones(v: any) -> Eones:
    if isinstance(v, Eones):
        return v
    return Eones(v)

EonesField = Annotated[Eones, BeforeValidator(validate_eones)]

class Event(BaseModel):
    name: str
    start_time: EonesField

# Usage
event = Event(name="Meeting", start_time="2025-10-01")
print(event.start_time.format("%Y-%m-%d"))  # 2025-10-01
```

## Response Serialization

Use the built-in `eones_encoder` from `eones.integrations.serializers` as the JSON encoder for FastAPI responses. It handles `Eones`, `Date`, and `Delta` objects automatically:

```python
import json
from eones.integrations.serializers import eones_encoder

# Works with json.dumps directly
data = {"start": Eones("2025-10-01"), "name": "Meeting"}
json.dumps(data, default=eones_encoder)
# {"start": "2025-10-01T00:00:00+00:00", "name": "Meeting"}
```

### With FastAPI's jsonable_encoder

```python
from fastapi.encoders import jsonable_encoder
from eones import Eones

json_compatible_item_data = jsonable_encoder(event, custom_encoder={
    Eones: lambda e: e.for_json()
})
```
