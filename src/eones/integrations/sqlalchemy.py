"""src/eones/integrations/sqlalchemy.py"""

from __future__ import annotations

from typing import Any, Optional

try:  # pragma: no cover - optional dependency
    from sqlalchemy.types import DateTime, TypeDecorator

    SQLALCHEMY_AVAILABLE = True
except ImportError:  # pragma: no cover - sqlalchemy not installed
    SQLALCHEMY_AVAILABLE = False

from eones.core.date import Date
from eones.interface import Eones

if SQLALCHEMY_AVAILABLE:

    class EonesType(TypeDecorator[Eones]):  # pylint: disable=too-many-ancestors
        """SQLAlchemy-compatible column type for storing Eones/Date instances.

        Persists as a standard ``DateTime`` column. On write, Date and Eones
        objects are converted to ``datetime``. On read, the stored value is
        returned as an ``Eones`` instance.
        """

        impl = DateTime
        cache_ok = True

        @property
        def python_type(self) -> type:
            """Return the Python type produced by this column type."""
            return Eones

        def process_literal_param(self, value: Any, _dialect: Any) -> Any:
            """Convert a literal bind value for inline rendering."""
            return self.process_bind_param(value, _dialect)

        def process_bind_param(self, value: Any, _dialect: Any) -> Any:
            """Convert an Eones or Date value to a datetime for storage.

            Args:
                value: An Eones, Date, datetime, or None.
                dialect: The SQLAlchemy dialect (unused).

            Returns:
                A datetime suitable for the database driver, or None.
            """
            if value is None:
                return None
            if isinstance(value, Eones):
                return value.to_datetime()
            if isinstance(value, Date):
                return value.to_datetime()
            return value

        def process_result_value(self, value: Any, _dialect: Any) -> Optional[Eones]:
            """Convert a database datetime to an Eones instance.

            Args:
                value: The datetime from the database, or None.
                dialect: The SQLAlchemy dialect (unused).

            Returns:
                Optional[Eones]: An Eones instance, or None.
            """
            if value is None:
                return None
            return Eones(value)

else:  # pragma: no cover - dummy placeholder

    class EonesType:  # type: ignore[no-redef]
        """Placeholder when SQLAlchemy is not installed."""
