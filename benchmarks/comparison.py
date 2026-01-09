import sys
import timeit
from datetime import datetime
from zoneinfo import ZoneInfo

from eones import Eones

# Try importing competitors
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


def bench_native():
    return datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))


def bench_eones():
    return Eones("2025-01-01")


def bench_pendulum():
    if pendulum:
        return pendulum.parse("2025-01-01")


def bench_arrow():
    if arrow:
        return arrow.get("2025-01-01")


def bench_delorean():
    if delorean:
        return delorean.parse("2025-01-01")


def bench_dateutil():
    if dateutil_parser:
        return dateutil_parser.parse("2025-01-01")


def run_benchmarks():
    print(f"Python {sys.version}")
    print("-" * 80)
    print(f"{'Library':<20} | {'Iterations':<10} | {'Time (s)':<10} | {'Ops/sec':<10}")
    print("-" * 80)
    benchmarks = [
        ("Native (datetime)", bench_native),
        ("Eones", bench_eones),
    ]

    if pendulum:
        benchmarks.append(("Pendulum", bench_pendulum))

    else:
        print("Skipping Pendulum (not installed)")

    if arrow:
        benchmarks.append(("Arrow", bench_arrow))

    else:
        print("Skipping Arrow (not installed)")

    if delorean:
        benchmarks.append(("Delorean", bench_delorean))

    else:
        print("Skipping Delorean (not installed)")

    if dateutil_parser:
        benchmarks.append(("dateutil", bench_dateutil))

    else:
        print("Skipping dateutil (not installed)")

    for name, func in benchmarks:
        number = 100_000
        # Reduce iterations for known slower libraries if custom logic needed,
        # but 100k is usually fine for parsed dates
        total_time = timeit.timeit(func, number=number)
        ops_sec = number / total_time
        print(f"{name:<20} | {number:<10} | {total_time:.4f}     | {ops_sec:,.0f}")


if __name__ == "__main__":
    run_benchmarks()
