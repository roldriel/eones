import gc
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from pympler import asizeof

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


def run_memory_bench():
    print(f"Python {sys.version}")
    print("-" * 60)
    print(f"{'Object Type':<20} | {'Size (bytes)':<10} | {'Notes':<20}")
    print("-" * 60)

    # Native
    dt = datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))
    size_native = asizeof.asizeof(dt)
    print(f"{'Native (datetime)':<20} | {size_native:<10} | {'Standard Lib'}")

    # Eones
    e = Eones("2025-01-01")
    size_eones = asizeof.asizeof(e)
    print(f"{'Eones (Facade)':<20} | {size_eones:<10} | {'Wrapper + Parser'}")

    d = e.now()
    size_date = asizeof.asizeof(d)
    print(f"{'Eones (Core)':<20} | {size_date:<10} | {'__slots__ optimized'}")

    # Pendulum
    if pendulum:
        p = pendulum.parse("2025-01-01")
        size_pendulum = asizeof.asizeof(p)
        print(f"{'Pendulum':<20} | {size_pendulum:<10} | {'Subclass of datetime'}")

    # Arrow
    if arrow:
        a = arrow.get("2025-01-01")
        size_arrow = asizeof.asizeof(a)
        print(f"{'Arrow':<20} | {size_arrow:<10} | {'Heavy Wrapper'}")

    # Delorean
    if delorean:
        d_obj = delorean.parse("2025-01-01")
        size_delorean = asizeof.asizeof(d_obj)
        print(f"{'Delorean':<20} | {size_delorean:<10} | {'Wrapper'}")

    print("-" * 60)
    print("\n[REAL WORLD METRIC] Marginal Cost Analysis (100k instances)")

    gc.collect()
    n = 100_000
    objs = [Eones("2025-01-01") for _ in range(n)]
    total_size = asizeof.asizeof(objs)
    avg_size = total_size / n

    # Calculate shared cost approximation
    # If 1 instance is size_eones (e.g. 368) and average is avg_size (e.g. 152)
    # The shared overhead is roughly (size_eones - avg_size)
    # This isn't perfect math because of list overhead, but it illustrates the point dynamically

    print(f"Because Eones shares one Parser for all standard instances, the")
    print(f"heavy components are paid ONCE. The real cost per object is:")
    print(f"Average Eones Size: {avg_size:.2f} bytes (Effective Footprint)")


if __name__ == "__main__":
    try:
        run_memory_bench()

    except ImportError:
        print("Please install 'pympler' to run memory benchmarks: pip install pympler")
