"""src/eones/integrations/django.py"""

from __future__ import annotations

from datetime import datetime
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
        """Custom Django model field that stores and retrieves Eones Date objects.

        Converts between Date and datetime when reading from and writing
        to the database. Supports form input via ``to_python``.
        """

        def from_db_value(
            self, value: Any, _expression: Any, _connection: Any
        ) -> Optional[Date]:
            """Convert a database datetime value to a Date instance.

            Args:
                value: The datetime value from the database.
                expression: The SQL expression (unused).
                connection: The database connection (unused).

            Returns:
                Optional[Date]: A Date instance, or None if the value is None.
            """
            if value is None:
                return None
            return Date(value)

        def to_python(self, value: Any) -> Optional[Date]:
            """Convert a value to a Date instance for form validation.

            Args:
                value: A string, datetime, Date, or None.

            Returns:
                Optional[Date]: A Date instance, or None.

            Raises:
                django.core.exceptions.ValidationError: If the value
                    cannot be converted.
            """
            if value is None:
                return None
            if isinstance(value, Date):
                return value
            value = super().to_python(value)
            if isinstance(value, datetime):
                return Date(value)
            return None

        def get_prep_value(self, value: Any) -> Any:
            """Convert a Date to a datetime for database storage.

            Args:
                value: A Date instance or any value accepted by the parent.

            Returns:
                A datetime suitable for the database driver.
            """
            if isinstance(value, Date):
                return value.to_datetime()
            return super().get_prep_value(value)

else:  # pragma: no cover - dummy placeholder

    class DateTimeField:  # type: ignore[no-redef]
        """Placeholder when Django is not installed."""
