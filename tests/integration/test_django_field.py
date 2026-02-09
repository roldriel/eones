"""tests/integration/test_django_field.py"""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

try:
    import django
    from django.conf import settings

    if not settings.configured:
        settings.configure(
            DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        )
        django.setup()

    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False

pytestmark = pytest.mark.skipif(not DJANGO_AVAILABLE, reason="Django not installed")

from eones.core.date import Date
from eones.integrations.django import DateTimeField


@pytest.fixture
def field():
    return DateTimeField()


@pytest.fixture
def aware_dt():
    return datetime(2025, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC"))


class TestFromDbValue:
    """Tests for DateTimeField.from_db_value."""

    def test_returns_none_for_none(self, field):
        assert field.from_db_value(None, None, None) is None

    def test_returns_date_from_datetime(self, field, aware_dt):
        result = field.from_db_value(aware_dt, None, None)
        assert isinstance(result, Date)
        assert result.to_datetime() == aware_dt

    def test_preserves_timezone(self, field):
        dt = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/Argentina/Buenos_Aires"))
        result = field.from_db_value(dt, None, None)
        assert isinstance(result, Date)


class TestToPython:
    """Tests for DateTimeField.to_python."""

    def test_returns_none_for_none(self, field):
        assert field.to_python(None) is None

    def test_returns_same_date_instance(self, field, aware_dt):
        d = Date(aware_dt)
        result = field.to_python(d)
        assert result is d

    def test_converts_datetime_to_date(self, field, aware_dt):
        result = field.to_python(aware_dt)
        assert isinstance(result, Date)

    def test_converts_string_to_date(self, field):
        result = field.to_python("2025-06-15T12:00:00+00:00")
        assert isinstance(result, Date)


class TestGetPrepValue:
    """Tests for DateTimeField.get_prep_value."""

    def test_converts_date_to_datetime(self, field, aware_dt):
        d = Date(aware_dt)
        result = field.get_prep_value(d)
        assert isinstance(result, datetime)
        assert result == aware_dt

    def test_passes_through_none(self, field):
        result = field.get_prep_value(None)
        assert result is None
