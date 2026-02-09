# 🧾 Comparison with other libraries

## Why not Pendulum or Arrow?

| Feature                                 | Eones | Pendulum | Arrow | Delorean | dateutil | pytz |
|-----------------------------------------|:-----:|:--------:|:-----:|:--------:|:--------:|:----:|
| Modern timezone support                | ✅ (`zoneinfo`) | ❌ (`pytz`) | ❌ (`pytz`) | ✅ | ⚠️ | ✅ |
| External dependencies                   | ✅ None | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes |
| Semantically rich API                   | ✅ Rich | ✅ Medium | ✅ Medium | ⚠️ | ❌ | ❌ |
| Modular/facade architecture             | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Complete type hinting & PEP 561         | ✅ Yes | ❌ Limited | ❌ Limited | ❌ No | ❌ No | ❌ No |
| **High Performance (>1.3M ops/sec)**      | **✅ Yes** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Memory Optimized (`__slots__`)**      | **✅ Yes** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Zero-dep Localization (No Babel)        | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Dedicated Range/Period API              | ✅ Yes | ✅ Yes | ⚠️ Basic | ⚠️ Basic | ❌ No | ❌ No |
| Date arithmetic (add/subtract)          | ✅    | ✅        | ✅    | ✅        | ❌        | ❌   |
| Flexible parsing (string, dict, dt)     | ✅    | ✅        | ✅    | ⚠️        | ✅        | ❌   |
| Coverage tested ≥ 97%                   | ✅    | ❓        | ❓    | ❌        | ❌        | ❌   |
| Can replace native `datetime` directly  | ✅    | ✅        | ✅    | ❌        | ❌        | ❌   |
| Permissive license (MIT / BSD)          | ✅    | ✅        | ✅    | ✅        | ✅        | ✅   |
| Actively maintained                     | ✅    | ✅        | ✅    | ❌        | ✅        | ⚠️   |

> **See the numbers yourself:** For detailed performance metrics (Speed, Memory, Profiling), check out our **[Benchmark Suite](https://github.com/roldriel/eones/blob/master/benchmarks/README.md)**.
