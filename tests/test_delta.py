from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eones.core.date import Date
from eones.core.delta import Delta

# ==== DIFF COMPATIBILITY ====


@pytest.mark.parametrize(
    "other, expected",
    [
        ("2025-01-03", 366),
        (Date(datetime(2025, 1, 3, tzinfo=ZoneInfo("UTC"))), 366),
        ({"year": 2025, "month": 1, "day": 3}, 366),
        (datetime(2025, 1, 3, tzinfo=ZoneInfo("UTC")), 366),
    ],
)
def test_diff_accepts_multiple_formats(other, expected):
    d1 = Date(datetime(2024, 1, 3, tzinfo=ZoneInfo("UTC")), tz="UTC")
    if isinstance(other, str):
        d2 = Date.from_iso(other)
    elif isinstance(other, dict):
        d2 = Date(
            datetime(
                other["year"], other["month"], other["day"], tzinfo=ZoneInfo("UTC")
            ),
            tz="UTC",
        )
    elif isinstance(other, datetime):
        d2 = Date(other, tz="UTC")
    else:
        d2 = other
    assert d2.diff(d1, unit="days") == expected


# ==== DIFF UNITS ====


@pytest.mark.parametrize(
    "start, end, unit, expected",
    [
        (
            datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")),
            datetime(2025, 1, 3, tzinfo=ZoneInfo("UTC")),
            "days",
            368,
        ),
        (
            datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")),
            datetime(2025, 1, 3, tzinfo=ZoneInfo("UTC")),
            "months",
            12,
        ),
        (
            datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")),
            datetime(2025, 1, 3, tzinfo=ZoneInfo("UTC")),
            "years",
            1,
        ),
    ],
)
def test_diff_units(start, end, unit, expected):
    d1 = Date(start, tz="UTC")
    d2 = Date(end, tz="UTC")
    assert d2.diff(d1, unit=unit) == expected


def test_delta_repr_and_equality():
    a = Delta(years=1, months=2, days=3)
    b = Delta(years=1, months=2, days=3)
    c = Delta(years=2)
    assert repr(a).startswith("Delta(")
    assert str(a) == "1y 2mo 3d"
    assert a.to_dict() == b.to_dict()
    assert a.to_dict() != c.to_dict()


def test_delta_apply_result():
    base = Date(datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")), tz="UTC")
    delta = Delta(years=1, months=1, days=1)
    result = delta.apply(base).to_datetime()
    expected = datetime(2025, 2, 2, tzinfo=ZoneInfo("UTC"))
    assert result == expected


# ==== DELTA COMPARISON AGAINST NON-DELTA ====


def test_delta_comparison_invalid_type():
    delta = Delta(days=1)
    assert (delta == "non-delta") is False


def test_init_valid_fields():
    delta = Delta(years=1, weeks=2)
    assert delta._calendar.years == 1
    assert delta._duration.to_input_dict()["weeks"] == 2


def test_init_invalid_key():
    with pytest.raises(ValueError) as e:
        Delta(foo=1)
    assert "Invalid delta fields" in str(e.value)


def test_init_invalid_type():
    with pytest.raises(TypeError):
        Delta(days="1")
    with pytest.raises(TypeError):
        Delta(hours=True)


def test_repr_nonzero():
    delta = Delta(months=3, minutes=5)
    assert repr(delta) == "Delta(months=3, minutes=5)"


def test_repr_zero():
    assert repr(Delta()) == "Delta(0s)"


def test_eq_same():
    d1 = Delta(years=1, days=2)
    d2 = Delta(years=1, days=2)
    assert d1._calendar.to_input_dict() == d2._calendar.to_input_dict()
    assert d1._duration.to_input_dict() == d2._duration.to_input_dict()


def test_eq_different():
    d1 = Delta(years=1)
    d2 = Delta(months=1)
    assert d1 != d2


def test_eq_invalid_type():
    assert Delta() != "not a Delta"


def test_hash_consistency():
    d1 = Delta(months=2, minutes=30)
    d2 = Delta(months=2, minutes=30)
    assert hash(d1) == hash(d2)


def test_str_compact_output():
    delta = Delta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
    assert str(delta) == "1y 2mo 3d 4h 5m 6s"


def test_str_zero():
    assert str(Delta()) == "0s"


def test_apply_calendar_only():
    base = Date.from_iso("2024-01-01")
    delta = Delta(months=1)
    result = delta.apply_calendar(base)
    assert result.to_iso() == "2024-02-01T00:00:00+00:00"


def test_apply_duration_only():
    base = Date.from_iso("2024-01-01T00:00:00")
    delta = Delta(hours=1)
    result = delta.apply_duration(base)
    assert result.to_iso() == "2024-01-01T01:00:00+00:00"


def test_apply_full():
    base = Date.from_iso("2024-01-01T00:00:00")
    delta = Delta(months=1, hours=1)
    result = delta.apply(base)
    assert result.to_iso() == "2024-02-01T01:00:00+00:00"


def test_apply_invalid_type():
    delta = Delta()
    with pytest.raises(TypeError):
        delta.apply("not a date")


def test_invert():
    d = Delta(years=1, days=2, hours=3)
    inv = d.invert()
    assert inv.to_input_dict() == {"years": -1, "days": -2, "hours": -3}


def test_scale():
    d = Delta(months=2, minutes=30)
    scaled = d.scale(2)
    assert scaled.to_input_dict() == {"months": 4, "minutes": 60}


def test_is_zero_true():
    assert Delta().is_zero()


def test_is_zero_false():
    assert not Delta(days=1).is_zero()


def test_to_iso_full():
    d = Delta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
    assert d.to_iso() == "P1Y2M3DT4H5M6S"


def test_to_iso_date_only():
    d = Delta(years=1, months=2, days=3)
    assert d.to_iso() == "P1Y2M3D"


def test_to_iso_time_only():
    d = Delta(hours=1, minutes=2, seconds=3)
    assert d.to_iso() == "PT1H2M3S"


def test_to_iso_empty():
    assert Delta().to_iso() == "P"


def test_from_iso_full():
    d = Delta.from_iso("P1Y2M3DT4H5M6S")
    assert d.to_input_dict() == {
        "years": 1,
        "months": 2,
        "days": 3,
        "hours": 4,
        "minutes": 5,
        "seconds": 6,
    }


def test_from_iso_date_only():
    d = Delta.from_iso("P3Y1M")
    assert d.to_input_dict() == {"years": 3, "months": 1}


def test_from_iso_time_only():
    d = Delta.from_iso("PT2H45M")
    assert d.to_input_dict() == {"hours": 2, "minutes": 45}


def test_from_iso_invalid():
    with pytest.raises(ValueError):
        Delta.from_iso("XYZ")
