from eones import add_days, format_date, parse_date, to_timestamp


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
