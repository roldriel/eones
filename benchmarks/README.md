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

## Key Results (v1.3.x)

### Overall Speed (Comparison)

This benchmark measures the speed of **parsing an ISO-8601 date** (`"2025-01-01"`), one of the most frequent and costly operations.
*   **Metric:** Operations per second (Ops/sec). Higher is better.
*   **Context:** `datetime` (Native) is the gold standard (written in C). `Eones` aims to get as close as possible to this theoretical limit, significantly outperforming other high-level libraries.

| Library | Ops/sec | Relative |
| :--- | :--- | :--- |
| **Native (datetime)** | 2,040,000 | 11.0x |
| **Eones** | **975,000** | **5.2x** |
| Pendulum | 186,000 | 1.0x (Base) |
| dateutil | 52,000 | 0.28x |
| Delorean | 43,000 | 0.23x |
| Arrow | 39,000 | 0.21x |

> *Note: Eones is approximately 5 times faster than Pendulum in standard parsing operations.*

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
| **Native (datetime)** | 0.0552 | 1,811,693 |
| **Eones** | 0.0457 | 1,094,300 |
| Pendulum | 0.2542 | 196,719 |
| dateutil | 1.0529 | 47,489 |
| Delorean | 1.1076 | 45,144 |
| Arrow | 1.2184 | 41,036 |

#### Arithmetic (+1 Day)
Time it takes to add a `timedelta` (e.g., `+ 1 day`). Here `Eones` is slower than native due to immutability and extra validations, but remains performant.

| Library | Time (s) | Ops/sec |
| :--- | :--- | :--- |
| **Native (datetime)** | 0.0447 | 1,118,000 |
| Eones | 0.4044 | 123,640 |
| Pendulum | 0.5406 | 92,485 |
| Delorean | 1.9439 | 25,721 |
| Arrow | 2.1013 | 23,795 |

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
   100000    0.081    0.000    0.243    0.000 interface.py:31(__init__) # Main constructor
   100000    0.074    0.000    0.130    0.000 date.py:476(from_iso)     # Optimized ISO parsing
   100000    0.018    0.000    0.018    0.000 {method 'count' of 'str'} # Internal string validation
   100000    0.018    0.000    0.018    0.000 {built-in fromisoformat}  # Native C call
```
