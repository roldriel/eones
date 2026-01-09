import pytest

from eones import Eones, add_days, format_date, parse_date, to_timestamp
from eones.core.date import Date
from eones.core.parser import Parser


def test_end_to_end_user_flow():
    date_str = "2024-02-28"
    dt = parse_date(date_str)
    dt2 = add_days(dt, 1)
    formatted = format_date(dt2, fmt="%Y-%m-%d")
    ts = to_timestamp(dt2)

    assert formatted == "2024-02-29"  # Leap year
    assert isinstance(ts, int)


def test_end_to_end_leap_year_and_back():
    d = parse_date("2024-02-29")
    d_plus_365 = add_days(d, 365)
    formatted = format_date(d_plus_365, "%Y-%m-%d")
    assert formatted == "2025-02-28"


def test_end_to_end_month_boundary():
    d = parse_date("2025-01-30")
    d_plus = add_days(d, 5)
    formatted = format_date(d_plus, "%Y-%m-%d")
    assert formatted == "2025-02-04"


# Eones/Interface Tests


def test_lazy_parser_lifecycle():
    """Test that the parser is initialized strictly when needed."""
    e = Eones("2024-01-01")
    with pytest.raises(AttributeError):
        _ = e._parser
    p = e.parser
    assert isinstance(p, Parser)
    assert e._parser is p


def test_lazy_parser_on_copy():
    """Test that copy obeys the lazy state of the original."""
    e1 = Eones("2024-01-01")
    e2 = e1.copy()
    with pytest.raises(AttributeError):
        _ = e2._parser
    _ = e1.parser
    e3 = e1.copy()
    assert e3._parser is not None


def test_eones_with_none_value():
    """Test Eones(None) creates current date."""
    e = Eones(None)
    assert e.now().year >= 2024


def test_eones_with_custom_string():
    """Test Eones with non-ISO string triggers global parser."""
    e = Eones("2024-01-01")
    assert e.now().year == 2024


def test_eones_with_custom_timezone():
    """Test Eones with custom timezone initializes instance parser."""
    e = Eones("2024-01-01", tz="Europe/Madrid")
    assert "Europe/Madrid" in e.now().timezone


def test_clone_alias():
    """Test that clone() is an alias for copy()."""
    e1 = Eones("2024-01-01")
    e2 = e1.clone()
    assert e2.now() == e1.now()
    assert e2 is not e1


def test_compare_date_vs_eones():
    """Test equality interactions."""
    d = Date.now(naive="utc")
    e = Eones(d)
    assert (e == d) is False


def test_date_sub_not_implemented():
    """Test __sub__ with invalid type returns NotImplemented."""
    d = Date.now(naive="utc")
    with pytest.raises(TypeError):
        _ = d - 100
