"""src/eones/integrations/sqlalchemy.py"""

from typing import Any

try:  # pragma: no cover - optional dependency
    from sqlalchemy.types import DateTime, TypeDecorator

    SQLALCHEMY_AVAILABLE = True
except ImportError:  # pragma: no cover - sqlalchemy not installed
    SQLALCHEMY_AVAILABLE = False
    DateTime = object  # type: ignore[assignment,misc]
    TypeDecorator = object  # type: ignore[assignment,misc]


from eones import Eones


class EonesType(TypeDecorator):  # type: ignore[type-arg]
    """SQLAlchemy-compatible type for storing Eones instances."""

    impl = DateTime

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if isinstance(value, Eones):
            return value.to_datetime()
        return value

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        return Eones(value)
