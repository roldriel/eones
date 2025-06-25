try:  # pragma: no cover - optional dependency
    from sqlalchemy.types import DateTime, TypeDecorator
except Exception:  # pragma: no cover - sqlalchemy not installed
    DateTime = object  # type: ignore

    class TypeDecorator:  # type: ignore
        pass


from eones import Eones


class EonesType(TypeDecorator):
    """SQLAlchemy-compatible type for storing Eones instances."""

    impl = DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, Eones):
            return value.to_datetime()
        return value

    def process_result_value(self, value, dialect):
        return Eones(value)
