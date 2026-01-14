import cProfile
import pstats

from eones import Eones


def run_profile():
    # Warmup
    Eones("2025-01-01")

    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(100000):
        Eones("2025-01-01")
    profiler.disable()

    with open("profiling.txt", "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs()
        stats.sort_stats(
            "tottime"
        )  # Sort by internal time to find the bottleneck function
        stats.print_stats(30)


if __name__ == "__main__":
    run_profile()
