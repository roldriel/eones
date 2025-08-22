from eones import date_range, format_date, parse_date


def test_date_range_integration():
    start = parse_date("2025-07-01")
    end = parse_date("2025-07-05")
    dates = date_range(start, end, step_days=1)
    formatted_dates = [format_date(d, "%Y-%m-%d") for d in dates]
    assert formatted_dates == [
        "2025-07-01",
        "2025-07-02",
        "2025-07-03",
        "2025-07-04",
        "2025-07-05",
    ]


def test_date_range_with_custom_step():
    start = parse_date("2025-07-01")
    end = parse_date("2025-07-05")
    dates = date_range(start, end, step_days=2)
    formatted_dates = [format_date(d, "%Y-%m-%d") for d in dates]
    assert formatted_dates == [
        "2025-07-01",
        "2025-07-03",
        "2025-07-05",
    ]


def test_date_range_start_equals_end():
    start = parse_date("2025-07-01")
    dates = date_range(start, start, step_days=1)
    formatted_dates = [format_date(d, "%Y-%m-%d") for d in dates]
    assert formatted_dates == ["2025-07-01"]
