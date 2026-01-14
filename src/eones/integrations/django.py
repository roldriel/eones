"""src/eones/integrations/django.py"""

from typing import Any, Optional

try:  # pragma: no cover - optional dependency
    from django.db import models

    DJANGO_AVAILABLE = True
except ImportError:  # pragma: no cover - django not installed
    DJANGO_AVAILABLE = False
    models = None

from eones.core.date import Date

if DJANGO_AVAILABLE and models is not None:

    class DateTimeField(models.DateTimeField):  # type: ignore[misc]
        """Custom Django model field to store Date as DateTime."""

        def from_db_value(
            self, value: Any, expression: Any, connection: Any
        ) -> Optional[Date]:
            if value is None:
                return value
            return Date(value)

        def get_prep_value(self, value: Any) -> Any:
            if isinstance(value, Date):
                return value.to_datetime()
            return super().get_prep_value(value)

else:  # pragma: no cover - dummy placeholder

    class DateTimeField:  # type: ignore[no-redef]
        pass
