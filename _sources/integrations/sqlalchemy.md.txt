# SQLAlchemy Integration

You can persist `Eones` or `Date` objects transparently using SQLAlchemy's `TypeDecorator`.

## Custom Column Type

Here is a recipe for a generic `EonesDateTime` column that stores data as UTC `DateTime` in the database but exposes `Date` (from Eones) in your models.

```python
from sqlalchemy import TypeDecorator, DateTime
from eones import Date
from datetime import datetime
from zoneinfo import ZoneInfo

class EonesDateTime(TypeDecorator):
    """
    Stores Eones Date as a timezone-naive UTC DateTime in the database.
    Retrieved as a timezone-aware Date (UTC) in Python.
    """
    impl = DateTime(timezone=False)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, Date):
            # Convert to UTC datetime for storage
            return value.as_utc().replace(tzinfo=None)
        if isinstance(value, datetime):
            return value.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # value is a naive datetime from DB (assumed UTC)
        # return as Date with UTC timezone
        return Date(value, tz="UTC", naive="utc")

# Usage in Models
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[Date] = mapped_column(EonesDateTime)

# The 'created_at' field will now automatically be a Eones Date object
```
