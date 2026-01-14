# Eones Benchmark Suite

This directory contains a comprehensive set of tools to evaluate the performance, memory usage, and behavior of `Eones`.

## Directory Structure

In a professional environment, benchmarks are organized by purpose:

1.  **Comparison (`comparison.py`):**
    *   **Purpose:** Evaluate `Eones` against competitors (`datetime`, `pendulum`, `arrow`, `dateutil`).
    *   **Use:** Marketing, competitive validation.
    *   **Execute:** `python comparison.py`

2.  **Micro-benchmarks (`microbenchmarks.py`):**
    *   **Purpose:** Measure the performance of specific methods (instantiation, arithmetic, formatting) in isolation.
    *   **Use:** Regression detection during development.
    *   **Execute:** `python microbenchmarks.py`

3.  **Profiling (`profiling.py`):**
    *   **Purpose:** Deep analysis of where CPU time is spent (call stacks).
    *   **Use:** Bottleneck optimization.
    *   **Execute:** `python profiling.py`

4.  **Memory (`memory.py`):**
    *   **Purpose:** Measure the memory footprint (bytes) of objects.
    *   **Use:** Verify the effectiveness of `__slots__`.
    *   **Execute:** `python memory.py` (Requires `pympler`)

## Requirements

Install necessary dependencies:

```bash
pip install -r comparison_requirements.txt
```

## Key Results (v1.5.x)

### Overall Speed (Comparison)

This benchmark measures the speed of **parsing an ISO-8601 date** (`"2025-01-01"`), one of the most frequent and costly operations.
*   **Metric:** Operations per second (Ops/sec). Higher is better.
*   **Context:** `datetime` (Native) is the gold standard (written in C). `Eones` aims to get as close as possible to this theoretical limit, significantly outperforming other high-level libraries.

| Library | Ops/sec | Relative |
| :--- | :--- | :--- |
| **Native (datetime)** | 2,052,000 | 10.2x |
| **Eones** | **1,347,000** | **6.7x** |
| Pendulum | 201,000 | 1.0x (Base) |
| dateutil | 54,000 | 0.27x |
| Delorean | 44,000 | 0.22x |
| Arrow | 41,000 | 0.20x |

> *Note: Eones is approximately 6.7 times faster than Pendulum in standard parsing operations.*

### Memory Usage

This table shows the **RAM memory footprint** of a single instance. Python has significant per-object overhead; `Eones` minimizes this using `__slots__` and sharing heavy components.

*   **Eones (Scaled):** The actual per-object cost when you have many instances (e.g., 100k dates in a list). `Eones` shares the parser engine (`Parser`) across all instances, drastically reducing total consumption.
*   **Eones (Isolated):** The cost of creating a *single* isolated date. Includes the weight of the `Parser` that is initialized for the first time.

| Object | Size (Bytes) | Notes |
| :--- | :--- | :--- |
| **Native (datetime)** | 48 | Python standard (C structure) |
| **Eones (Scaled)** | **152** | **Real average cost (Shared State)** |
| **Eones (Isolated)** | 368 | First instance (Init Parser) |
| Pendulum | 384 | datetime subclass (+ overhead) |
| Arrow | 432 | Heavy wrapper |
| Delorean | 840 | Very heavy wrapper |

---

### Micro-Operations

Detailed breakdown of specific actions to identify internal bottlenecks.

#### Construction
Time it takes to create an object from scratch.

| Library | Time (s) | Ops/sec |
| :--- | :--- | :--- |
| **Native (datetime)** | 0.0486 | 2,058,765 |
| **Eones** | 0.0757 | 1,320,151 |
| Pendulum | 0.5153 | 194,068 |
| dateutil | 1.8738 | 53,369 |
| Delorean | 2.2165 | 45,117 |
| Arrow | 2.4377 | 41,022 |

#### Arithmetic (+1 Day)
Time it takes to add a `timedelta` (e.g., `+ 1 day`). Here `Eones` is slower than native due to immutability and extra validations, but remains performant.

| Library | Time (s) | Ops/sec |
| :--- | :--- | :--- |
| **Native (datetime)** | 0.0846 | 1,182,103 |
| Eones | 0.1614 | 619,625 |
| Pendulum | 1.0518 | 95,073 |
| Delorean | 3.9112 | 25,568 |
| Arrow | 4.1812 | 23,916 |

---

### Profiling of Eones

This section analyzes **Eones exclusively** to identify which parts of our internal code consume the most CPU.

**Legend:**
*   **filename:lineno(function):** Source code file of `Eones` where the operation occurs.
    *   `interface.py`: Public layer of the library.
    *   `date.py`: Core logic (Date).
*   **ncalls:** Number of times the function was called.
*   **tottime:** Total time spent INSIDE that function (excluding calls to other functions).
*   **percall:** Average time per call.

**Results (100k object instantiation):**

```text
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   100000    0.075    0.000    0.192    0.000 interface.py:46(__init__)
   100000    0.053    0.000    0.091    0.000 date.py:512(from_iso)
   100000    0.018    0.000    0.018    0.000 {built-in method fromisoformat}
   200000    0.015    0.000    0.015    0.000 {built-in method builtins.len}
```
