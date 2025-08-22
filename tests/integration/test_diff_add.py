from eones import add_days, date_diff_days, format_date, parse_date


def test_diff_between_parsed_dates():
    d1 = parse_date("2025-07-01")
    d2 = parse_date("2025-07-11")
    diff = date_diff_days(d1, d2)
    assert diff == 10


def test_add_days_and_check_diff():
    d = parse_date("2025-07-01")
    d_plus = add_days(d, 5)
    diff = date_diff_days(d, d_plus)
    assert diff == 5


def test_add_negative_days():
    d = parse_date("2025-07-11")
    d_minus = add_days(d, -10)
    formatted = format_date(d_minus, "%Y-%m-%d")
    assert formatted == "2025-07-01"


def test_diff_same_day_returns_zero():
    d = parse_date("2025-07-11")
    diff = date_diff_days(d, d)
    assert diff == 0
