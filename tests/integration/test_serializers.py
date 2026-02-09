"""tests/integration/test_serializers.py"""

import json

import pytest

from eones import Eones
from eones.core.date import Date
from eones.core.delta import Delta
from eones.integrations.serializers import eones_encoder


class TestEonesEncoderDate:
    """Tests for eones_encoder with Date objects."""

    def test_encodes_date_to_iso_string(self):
        d = Date()
        result = eones_encoder(d)
        assert isinstance(result, str)
        assert "T" in result

    def test_date_roundtrip_via_json_dumps(self):
        d = Date()
        output = json.dumps({"date": d}, default=eones_encoder)
        parsed = json.loads(output)
        assert parsed["date"] == d.to_iso()


class TestEonesEncoderEones:
    """Tests for eones_encoder with Eones objects."""

    def test_encodes_eones_to_iso_string(self):
        e = Eones("2025-06-15")
        result = eones_encoder(e)
        assert isinstance(result, str)
        assert "2025-06-15" in result

    def test_eones_roundtrip_via_json_dumps(self):
        e = Eones("2025-03-01T10:00:00+00:00")
        output = json.dumps({"ts": e}, default=eones_encoder)
        parsed = json.loads(output)
        assert parsed["ts"] == e.for_json()


class TestEonesEncoderDelta:
    """Tests for eones_encoder with Delta objects."""

    def test_encodes_delta_to_iso_string(self):
        delta = Delta(days=5, hours=3)
        result = eones_encoder(delta)
        assert result == "P5DT3H"

    def test_delta_with_years_and_months(self):
        delta = Delta(years=1, months=2)
        result = eones_encoder(delta)
        assert result == "P1Y2M"

    def test_delta_roundtrip_via_json_dumps(self):
        delta = Delta(days=10)
        output = json.dumps({"delta": delta}, default=eones_encoder)
        parsed = json.loads(output)
        assert parsed["delta"] == "P10D"


class TestEonesEncoderErrors:
    """Tests for eones_encoder with unsupported types."""

    def test_raises_type_error_for_unsupported_type(self):
        with pytest.raises(TypeError, match="object"):
            eones_encoder(object())

    def test_raises_type_error_for_string(self):
        with pytest.raises(TypeError, match="str"):
            eones_encoder("not a date")

    def test_raises_type_error_for_int(self):
        with pytest.raises(TypeError, match="int"):
            eones_encoder(42)


class TestEonesEncoderNested:
    """Tests for eones_encoder with nested structures."""

    def test_mixed_types_in_dict(self):
        data = {
            "date": Date(),
            "eones": Eones("2025-01-01"),
            "delta": Delta(hours=2),
            "plain": "text",
        }
        output = json.dumps(data, default=eones_encoder)
        parsed = json.loads(output)
        assert isinstance(parsed["date"], str)
        assert isinstance(parsed["eones"], str)
        assert parsed["delta"] == "PT2H"
        assert parsed["plain"] == "text"
