from django.db import models

from eones.core.date import EonesDate


class EonesDateTimeField(models.DateTimeField):
    """Custom Django model field to store EonesDate as DateTime."""

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return EonesDate(value)

    def get_prep_value(self, value):
        if isinstance(value, EonesDate):
            return value.to_datetime()
        return super().get_prep_value(value)
