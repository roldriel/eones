# FastAPI & Pydantic Integration

Eones works seamlessly with FastAPI and Pydantic. You can create custom types to automatically validate and serialize dates.

## Custom Pydantic Type

To use `Eones` or `Date` as a Pydantic field, you can define an annotated type with a `BeforeValidator` or a custom class with `__get_pydantic_core_schema__`.

### Simple Validator Approach

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

To ensure Eones objects are serialized correctly to JSON in FastAPI responses, you can configure your Pydantic models to use a custom encoder or simply ensure your `Eones` objects are converted to strings/IS0 formats before return, or register a custom encoder in FastAPI.

```python
from fastapi.encoders import jsonable_encoder

# ...
json_compatible_item_data = jsonable_encoder(event, custom_encoder={
    Eones: lambda e: e.to_iso()
})
```
