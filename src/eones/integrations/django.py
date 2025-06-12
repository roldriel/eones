from django.db import models

from eones.core.date import Date


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
