"""Django integration helpers (optional)."""

try:  # pragma: no cover - optional dependency
    from django.db import models
except Exception:  # pragma: no cover - django not installed
    models = None  # type: ignore

from eones.core.date import Date

if models is not None:

    class DateTimeField(models.DateTimeField):
        """Custom Django model field to store Date as DateTime."""

        def from_db_value(self, value, expression, connection):
            if value is None:
                return value
            return Date(value)

        def get_prep_value(self, value):
            if isinstance(value, Date):
                return value.to_datetime()
            return super().get_prep_value(value)

else:  # pragma: no cover - dummy placeholder

    class DateTimeField:  # type: ignore
        pass
