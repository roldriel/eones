"""src/eones/integrations/sqlalchemy.py"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

try:  # pragma: no cover - optional dependency
    from sqlalchemy.types import DateTime as _DateTime
    from sqlalchemy.types import TypeDecorator as _TypeDecorator

    _SQLALCHEMY_AVAILABLE = True
except ImportError:  # pragma: no cover - sqlalchemy not installed
    _SQLALCHEMY_AVAILABLE = False
    _DateTime = None  # type: ignore[misc,assignment]  # optional dep fallback

from eones.core.date import Date
from eones.interface import Eones

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.types import TypeDecorator

    _Base = TypeDecorator[Eones]
else:
    _Base = _TypeDecorator if _SQLALCHEMY_AVAILABLE else object


class EonesType(_Base):  # pylint: disable=too-many-ancestors
    """SQLAlchemy-compatible column type for storing Eones/Date instances.

    Persists as a standard ``DateTime`` column. On write, Date and Eones
    objects are converted to ``datetime``. On read, the stored value is
    returned as an ``Eones`` instance.

    When SQLAlchemy is not installed the class is still importable but
    inherits from ``object`` so that type references do not break.
    """

    if _DateTime is not None:
        impl = _DateTime
    cache_ok = True

    @property
    def python_type(self) -> type:
        """Return the Python type produced by this column type."""
        return Eones

    def process_literal_param(self, value: Any, dialect: Any) -> Any:
        """Convert a literal bind value for inline rendering."""
        return self.process_bind_param(value, dialect)

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        """Convert an Eones or Date value to a datetime for storage.

        Args:
            value: An Eones, Date, datetime, or None.
            dialect: The SQLAlchemy dialect (unused).

        Returns:
            A datetime suitable for the database driver, or None.
        """
        del dialect
        if value is None:
            return None
        if isinstance(value, Eones):
            return value.to_datetime()
        if isinstance(value, Date):
            return value.to_datetime()
        return value

    def process_result_value(self, value: Any, dialect: Any) -> Optional[Eones]:
        """Convert a database datetime to an Eones instance.

        Args:
            value: The datetime from the database, or None.
            dialect: The SQLAlchemy dialect (unused).

        Returns:
            Optional[Eones]: An Eones instance, or None.
        """
        del dialect
        if value is None:
            return None
        return Eones(value)
