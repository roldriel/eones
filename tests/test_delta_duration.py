import pytest

from eones.core.delta_duration import DeltaDuration


def test_init_type_validation():
    with pytest.raises(TypeError):
        DeltaDuration(days="5")
    with pytest.raises(TypeError):
        DeltaDuration(hours=True)


def test_invert():
    delta = DeltaDuration(days=2, hours=3)
    inverted = delta.invert()
    assert inverted.to_input_dict() == {"days": -2, "hours": -3}


def test_scale():
    delta = DeltaDuration(days=1, minutes=30)
    scaled = delta.scale(2)
    assert scaled.to_input_dict() == {"days": 2, "minutes": 60}


def test_to_input_dict():
    delta = DeltaDuration(weeks=1, seconds=10)
    assert delta.to_input_dict() == {"weeks": 1, "seconds": 10}


def test_is_zero_true():
    assert DeltaDuration().is_zero()


def test_is_zero_false():
    assert not DeltaDuration(hours=1).is_zero()


def test_to_iso_full():
    delta = DeltaDuration(weeks=1, days=2, hours=3, minutes=4, seconds=5)
    assert delta.to_iso() == "P9DT3H4M5S"  # 1w + 2d = 9d


def test_to_iso_days_only():
    assert DeltaDuration(days=2).to_iso() == "P2D"


def test_to_iso_time_only():
    delta = DeltaDuration(hours=1, minutes=15, seconds=30)
    assert delta.to_iso() == "PT1H15M30S"


def test_to_iso_mixed():
    delta = DeltaDuration(days=1, minutes=45)
    assert delta.to_iso() == "P1DT45M"


def test_to_iso_zero():
    assert DeltaDuration().to_iso() == "P"


def test_from_iso_full():
    delta = DeltaDuration.from_iso("P1W2DT3H4M5S")
    assert delta.to_input_dict() == {
        "weeks": 1,
        "days": 2,
        "hours": 3,
        "minutes": 4,
        "seconds": 5,
    }


def test_from_iso_days_only():
    d = DeltaDuration.from_iso("P4D")
    assert d.to_input_dict() == {"days": 4}  # sin "weeks": 0


def test_from_iso_time_only():
    d = DeltaDuration.from_iso("PT2H30M")
    assert d.to_input_dict() == {"hours": 2, "minutes": 30}


def test_from_iso_mixed():
    d = DeltaDuration.from_iso("P2DT5M")
    assert d.to_input_dict() == {"days": 2, "minutes": 5}


def test_from_iso_invalid():
    with pytest.raises(ValueError):
        DeltaDuration.from_iso("XYZ")
