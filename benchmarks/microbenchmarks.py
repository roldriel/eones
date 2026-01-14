import sys
import timeit
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from eones import Date, Eones

try:
    import pendulum

except ImportError:
    pendulum = None

try:
    import arrow

except ImportError:
    arrow = None

try:
    import delorean

except ImportError:
    delorean = None

try:
    from dateutil import parser as dateutil_parser

except ImportError:
    dateutil_parser = None


def bench_construct_date():
    return Date(datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC")))


def bench_construct_native():
    return datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))


def bench_construct_eones():
    return Eones("2025-01-01")


def bench_construct_pendulum():
    return pendulum.parse("2025-01-01")


def bench_construct_arrow():
    return arrow.get("2025-01-01")


def bench_construct_delorean():
    return delorean.parse("2025-01-01")


def bench_construct_dateutil():
    return dateutil_parser.parse("2025-01-01")


def bench_add_day_eones():
    d = Eones("2025-01-01")
    d.add(days=1)
    return d


def bench_add_day_native():
    d = datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))
    return d + timedelta(days=1)


def bench_add_day_pendulum():
    d = pendulum.parse("2025-01-01")
    return d.add(days=1)


def bench_add_day_arrow():
    d = arrow.get("2025-01-01")
    return d.shift(days=1)


def bench_add_day_delorean():
    d = delorean.parse("2025-01-01")
    return d.next_day(1)


def run_benchmarks():
    print(f"Python {sys.version}")
    print("-" * 60)
    print(
        f"{'Benchmark':<30} | {'Iterations':<10} | {'Time (s)':<10} | {'Ops/sec':<10}"
    )
    print("-" * 60)

    benchmarks = [
        ("Construction (Native)", bench_construct_native),
        ("Construction (Date)", bench_construct_date),
        ("Construction (Eones)", bench_construct_eones),
    ]

    if pendulum:
        benchmarks.append(("Construction (Pendulum)", bench_construct_pendulum))

    if arrow:
        benchmarks.append(("Construction (Arrow)", bench_construct_arrow))

    if delorean:
        benchmarks.append(("Construction (Delorean)", bench_construct_delorean))

    if dateutil_parser:
        benchmarks.append(("Construction (dateutil)", bench_construct_dateutil))

    benchmarks.extend(
        [
            ("Add 1 Day (Native)", bench_add_day_native),
            ("Add 1 Day (Eones)", bench_add_day_eones),
        ]
    )

    if pendulum:
        benchmarks.append(("Add 1 Day (Pendulum)", bench_add_day_pendulum))

    if arrow:
        benchmarks.append(("Add 1 Day (Arrow)", bench_add_day_arrow))

    if delorean:
        benchmarks.append(("Add 1 Day (Delorean)", bench_add_day_delorean))

    for name, func in benchmarks:
        number = 100_000  # Reduced for slower libs
        total_time = timeit.timeit(func, number=number)
        ops_sec = number / total_time
        print(f"{name:<30} | {number:<10} | {total_time:.4f}     | {ops_sec:,.0f}")


if __name__ == "__main__":
    run_benchmarks()
