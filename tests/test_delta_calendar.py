import pytest

from eones.core.delta_calendar import DeltaCalendar


def test_init_type_validation():
    with pytest.raises(TypeError):
        DeltaCalendar(years="1")  # str no válido
    with pytest.raises(TypeError):
        DeltaCalendar(months=True)  # bool no válido


def test_invert():
    delta = DeltaCalendar(years=2, months=3)
    inverted = delta.invert()
    # total_months = -27 → -3 years, 9 months
    assert inverted.years == -3 and inverted.months == 9


def test_scale():
    delta = DeltaCalendar(years=1, months=2)
    scaled = delta.scale(2)
    assert scaled.years == 2 and scaled.months == 4


def test_to_input_dict():
    delta = DeltaCalendar(years=3, months=5)
    assert delta.to_input_dict() == {"years": 3, "months": 5}


def test_is_zero_true():
    delta = DeltaCalendar()
    assert delta.is_zero() is True


def test_is_zero_false():
    delta = DeltaCalendar(months=1)
    assert delta.is_zero() is False


def test_eq_same():
    a = DeltaCalendar(years=1, months=6)
    b = DeltaCalendar(years=1, months=6)
    assert a == b


def test_eq_different():
    a = DeltaCalendar(years=1, months=6)
    b = DeltaCalendar(years=2, months=0)
    assert a != b


def test_eq_non_delta_calendar():
    assert DeltaCalendar() != "not a delta"


def test_repr():
    delta = DeltaCalendar(years=1, months=2)
    assert repr(delta) == "DeltaCalendar(years=1, months=2)"


def test_to_iso_full():
    assert DeltaCalendar(1, 2).to_iso() == "P1Y2M"


def test_to_iso_years_only():
    assert DeltaCalendar(3, 0).to_iso() == "P3Y"


def test_to_iso_months_only():
    assert DeltaCalendar(0, 5).to_iso() == "P5M"


def test_to_iso_zero():
    assert DeltaCalendar(0, 0).to_iso() == "P0M"


def test_from_iso_full():
    delta = DeltaCalendar.from_iso("P2Y3M")
    assert delta.to_input_dict() == {"years": 2, "months": 3}


def test_from_iso_years_only():
    delta = DeltaCalendar.from_iso("P4Y")
    assert delta.to_input_dict() == {"years": 4, "months": 0}


def test_from_iso_months_only():
    delta = DeltaCalendar.from_iso("P8M")
    assert delta.to_input_dict() == {"years": 0, "months": 8}


def test_from_iso_zero():
    delta = DeltaCalendar.from_iso("P0M")
    assert delta.to_input_dict() == {"years": 0, "months": 0}


def test_from_iso_invalid():
    with pytest.raises(ValueError):
        DeltaCalendar.from_iso("PXYZ")
