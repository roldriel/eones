from datetime import datetime

import pytest

from eones import Eones
from eones.core.date import EonesDate
from eones.core.delta import EonSpan


@pytest.mark.parametrize(
    "other,expected",
    [
        ("2025-01-03", 366),
        (EonesDate(datetime(2025, 1, 3)), 366),
        ({"year": 2025, "month": 1, "day": 3}, 366),
        (datetime(2025, 1, 3), 366),
        (Eones("2025-01-03"), 366),
    ],
)
def test_eonesdelta_difference_variants(other, expected):
    result = EonesDate(datetime(2024, 1, 3))
    other_parsed = EonesDate(datetime(2025, 1, 3))
    assert other_parsed.diff(result, unit="days") == expected


@pytest.mark.parametrize(
    "unit,expected",
    [
        ("days", 368),
        ("months", 12),
        ("years", 1),
    ],
)
def test_eonesdelta_difference_units(unit, expected):
    result = Eones("2024-01-01").now()
    assert Eones("2025-01-03").now().diff(result, unit=unit) == expected


def test_eonesdelta_difference_invalid_unit():
    delta = EonesDate.from_iso("2024-01-03")
    other = EonesDate.from_iso("2025-01-03")
    with pytest.raises(ValueError, match="Unsupported unit"):
        delta.diff(other, unit="weeks")


def test_eonspan_repr_and_eq():
    span1 = EonSpan(years=1, months=2, days=3)
    span2 = EonSpan(years=1, months=2, days=3)
    span3 = EonSpan(years=2)
    assert repr(span1).startswith("EonSpan(")
    assert span1 == span2
    assert span1 != span3


def test_eonspan_apply_with_timedelta():
    base = EonesDate.from_iso("2024-01-01")
    span = EonSpan(years=1, months=1, days=1, hours=2)
    result = span.apply(base)
    assert isinstance(result, EonesDate)


def test_eonspan_invalid_argument():
    with pytest.raises(ValueError) as excinfo:
        EonSpan(weeks=1)  # 'weeks' no está permitido
    assert "Invalid time arguments" in str(excinfo.value)


def test_eonspan_equality_with_invalid_type():
    delta = EonSpan(days=1)
    assert (delta == "not-a-span") is False
