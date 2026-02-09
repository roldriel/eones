"""tests/integration/test_sqlalchemy_type.py"""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

try:
    import sqlalchemy

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not SQLALCHEMY_AVAILABLE, reason="SQLAlchemy not installed"
)

from eones import Eones
from eones.core.date import Date
from eones.integrations.sqlalchemy import EonesType


@pytest.fixture
def col_type():
    return EonesType()


@pytest.fixture
def aware_dt():
    return datetime(2025, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC"))


class TestCacheOk:
    """Tests for EonesType.cache_ok attribute."""

    def test_cache_ok_is_true(self):
        assert EonesType.cache_ok is True


class TestProcessBindParam:
    """Tests for EonesType.process_bind_param."""

    def test_returns_none_for_none(self, col_type):
        assert col_type.process_bind_param(None, None) is None

    def test_converts_eones_to_datetime(self, col_type, aware_dt):
        e = Eones(aware_dt)
        result = col_type.process_bind_param(e, None)
        assert isinstance(result, datetime)
        assert result == aware_dt

    def test_converts_date_to_datetime(self, col_type, aware_dt):
        d = Date(aware_dt)
        result = col_type.process_bind_param(d, None)
        assert isinstance(result, datetime)
        assert result == aware_dt

    def test_passes_through_raw_datetime(self, col_type, aware_dt):
        result = col_type.process_bind_param(aware_dt, None)
        assert result is aware_dt


class TestProcessResultValue:
    """Tests for EonesType.process_result_value."""

    def test_returns_none_for_none(self, col_type):
        assert col_type.process_result_value(None, None) is None

    def test_returns_eones_from_datetime(self, col_type, aware_dt):
        result = col_type.process_result_value(aware_dt, None)
        assert isinstance(result, Eones)
        assert result.to_datetime() == aware_dt

    def test_roundtrip_eones(self, col_type, aware_dt):
        e = Eones(aware_dt)
        stored = col_type.process_bind_param(e, None)
        restored = col_type.process_result_value(stored, None)
        assert isinstance(restored, Eones)
        assert restored.to_datetime() == aware_dt

    def test_roundtrip_date(self, col_type, aware_dt):
        d = Date(aware_dt)
        stored = col_type.process_bind_param(d, None)
        restored = col_type.process_result_value(stored, None)
        assert isinstance(restored, Eones)
        assert restored.to_datetime() == aware_dt
