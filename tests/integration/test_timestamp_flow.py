from eones import add_days, format_date, from_timestamp, parse_date, to_timestamp


def test_string_to_timestamp_to_string():
    date_str = "2025-07-11 10:30:00"
    dt = parse_date(date_str)
    ts = to_timestamp(dt)
    dt2 = from_timestamp(ts)
    final_str = format_date(dt2, fmt="%Y-%m-%d %H:%M:%S")
    assert final_str == date_str


def test_timestamp_and_add_days_consistency():
    d = parse_date("2025-07-11")
    ts = to_timestamp(d)
    d_from_ts = from_timestamp(ts)
    d_plus5 = add_days(d_from_ts, 5)
    d_expected = add_days(d, 5)
    assert d_plus5 == d_expected


def test_to_timestamp_returns_integer():
    d = parse_date("2025-07-11 10:30:00")
    ts = to_timestamp(d)
    assert isinstance(ts, int)
