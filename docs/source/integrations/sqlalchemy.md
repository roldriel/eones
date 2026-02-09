# SQLAlchemy Integration

Eones provides a built-in `EonesType` column type that transparently converts between `Eones`/`Date` objects and `DateTime` columns in SQLAlchemy.

## Built-in Column Type

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from eones.integrations.sqlalchemy import EonesType

class Base(DeclarativeBase):
    pass

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    starts_at: Mapped["Eones"] = mapped_column(EonesType)
```

### Writing to the database

`EonesType` accepts `Eones`, `Date`, or plain `datetime` values. They are converted to `datetime` before storage.

```python
from eones import Eones
from eones.core.date import Date

event = Event(
    name="Team meeting",
    starts_at=Eones("2025-06-15T10:00:00+00:00"),
)
session.add(event)
session.commit()
```

### Reading from the database

Values are automatically returned as `Eones` instances:

```python
event = session.get(Event, 1)
print(type(event.starts_at))  # <class 'eones.interface.Eones'>
print(event.starts_at.format("%Y-%m-%d %H:%M"))  # 2025-06-15 10:00
```

### Nullable columns

`EonesType` handles `None` values transparently for nullable columns:

```python
from typing import Optional

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    completed_at: Mapped[Optional["Eones"]] = mapped_column(EonesType, nullable=True)
```

## API Reference

### `EonesType`

- **`impl`**: `DateTime` &mdash; stores as a standard datetime column.
- **`cache_ok`**: `True` &mdash; safe for SQLAlchemy statement caching.
- **`process_bind_param(value, dialect)`**: Converts `Eones` or `Date` to `datetime` for storage. Passes `None` and raw `datetime` through unchanged.
- **`process_result_value(value, dialect)`**: Converts a `datetime` from the database to an `Eones` instance. Returns `None` for `NULL` values.
