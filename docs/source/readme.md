# Eones
![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![PyPI](https://img.shields.io/pypi/v/eones?style=for-the-badge)
![Pylint](https://img.shields.io/badge/pylint-10.00-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-100%25-red?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-manual-green?style=for-the-badge)
![Tox](https://img.shields.io/badge/Tested%20tox-yellowgreen?style=for-the-badge)

---

> Compatible with Python 3.9+ · No external dependencies · Portable and lightweight

---

## ✨ What is Eones?

Eones is a minimalist, dependency-free library for expressive, clear, and powerful date/time manipulation. Inspired by natural language semantics, it allows you to manipulate, compare, and transform dates as if they were living entities.

> *"That is not dead which can eternal lie, and with strange aeons even death may die."*  
> — *Abdul Alhazred*, Necronomicon

### Philosophy

> **Eones is not a datetime replacement. It's a temporal reasoning layer.**

Eones exists to fill the gap between Python's low-level `datetime` and the need for semantic, calendar-aware date manipulation:

- Using **only the standard library** (Python 3.9+)
- Providing a **semantically rich and consistent API**
- Supporting modern timezone-aware design with `zoneinfo`
- Maintaining **modular and composable** architecture through clear separation of responsibilities (`Date`, `Delta`, `Range`)

**Eones is for:**
- Developers who want to reason about time semantically, not just manipulate timestamps
- Teams that want **zero external dependencies** for maximum portability
- Projects where **timezones, truncation, deltas and ranges** are central domain logic

---

## 📦 Installation

```bash
pip install "eones"
```

> If you're working with timezones on Windows or containers:  
> ⚠️ Also install `tzdata`:
> ```bash
> pip install tzdata
> ```

---

## 🧪 Basic Example

```python
from eones import Eones

z = Eones("2025-06-15")
z.add(months=1, days=3)  # -> add 3 days and 1 month

print(z.format("%Y-%m-%d"))  # → 2025-07-18
print(z.diff_for_humans("2025-06-10"))  # → in 5 days
print(z.diff_for_humans("2025-06-20", locale="es"))  # → hace 5 días
```

---

## 🔍 Key Features

- ✅ **Zero external dependencies**: Pure Python (Python 3.9+)
- ✅ **Intuitive interface**: Simple, semantically rich and easy-to-use API
- ✅ **Modern timezone support**: Robust handling with `zoneinfo` (not `pytz`)
- ✅ **Flexible parsing**: Accepts multiple date formats automatically, including ISO 8601 with timezone offsets
- ✅ **Advanced temporal operations**: Deltas, ranges and semantic comparisons
- ✅ **Modular architecture**: Clear separation between `Date`, `Delta`, `Range` and utilities
- ✅ **Localization**: Support for multiple languages
- ✅ **Humanization**: Converts time differences to readable text
- ✅ **Complete type hinting**: Fully typed following PEP 561
- ✅ **Interoperability**: Compatible with Python's standard `datetime`

### Localization & Error Handling

You can add more languages by creating a new file in `eones/locales/` with the
translations for your locale. For example, `fr.py` for French.

Eones surfaces clear exceptions derived from `EonesError`. Invalid timezones
raise `InvalidTimezoneError`, while unparsable strings raise
`InvalidFormatError`.

---

## 🧾 Comparison with other libraries

### Why not Pendulum or Arrow?

| Feature                                 | Eones | Pendulum | Arrow | Delorean | dateutil | pytz |
|-----------------------------------------|:-----:|:--------:|:-----:|:--------:|:--------:|:----:|
| Modern timezone support                | ✅ (`zoneinfo`) | ❌ (`pytz`) | ❌ (`pytz`) | ✅ | ⚠️ | ✅ |
| External dependencies                   | ✅ None | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes |
| Semantically rich API                   | ✅ Rich | ✅ Medium | ✅ Medium | ⚠️ | ❌ | ❌ |
| Modular/facade architecture             | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Complete type hinting & PEP 561         | ✅ Yes | ❌ Limited | ❌ Limited | ❌ No | ❌ No | ❌ No |
| **High Performance (~1M ops/sec)**      | **✅ Yes** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Memory Optimized (`__slots__`)**      | **✅ Yes** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Zero-dep Localization (No Babel)        | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Dedicated Range/Period API              | ✅ Yes | ✅ Yes | ⚠️ Basic | ⚠️ Basic | ❌ No | ❌ No |
| Date arithmetic (add/subtract)          | ✅    | ✅        | ✅    | ✅        | ❌        | ❌   |
| Flexible parsing (string, dict, dt)     | ✅    | ✅        | ✅    | ⚠️        | ✅        | ❌   |
| Coverage tested ≥ 97%                   | ✅    | ❓        | ❓    | ❌        | ❌        | ❌   |
| Can replace native `datetime` directly  | ✅    | ✅        | ✅    | ❌        | ❌        | ❌   |
| Permissive license (MIT / BSD)          | ✅    | ✅        | ✅    | ✅        | ✅        | ✅   |
| Actively maintained                     | ✅    | ✅        | ✅    | ❌        | ✅        | ⚠️   |

> **See the numbers yourself:** For detailed performance metrics (Speed, Memory, Profiling), check out our **[Benchmark Suite](benchmarks/README.md)**.

---

## 📚 Documentation & Examples

Comprehensive examples and documentation are available:

### 📖 Core Examples
- **[Basic Usage](https://github.com/roldriel/eones/blob/master/examples/basic_usage.md)** - Library import, date creation, formatting, basic operations
- **[Advanced Usage](https://github.com/roldriel/eones/blob/master/examples/advanced_usage.md)** - Truncation, rounding, period ranges, comparisons
- **[Complete Deltas](https://github.com/roldriel/eones/blob/master/examples/complete_deltas.md)** - Dual delta architecture, calendar vs duration intervals
- **[Use Cases](https://github.com/roldriel/eones/blob/master/examples/use_cases.md)** - Real-world examples: age calculation, billing cycles, reports
- **[Error Handling](https://github.com/roldriel/eones/blob/master/examples/error_handling.md)** - Exception hierarchy, safe date creation, validation
- **[Formatting & Serialization](https://github.com/roldriel/eones/blob/master/examples/formatting_serialization.md)** - ISO 8601, JSON export/import, API integration
- **[Week Configuration](https://github.com/roldriel/eones/blob/master/examples/week_configuration.md)** - First day of week configuration, ISO vs US standards, weekend detection

### 🔗 Integration Examples
- **Django**: Custom model fields
- **SQLAlchemy**: Specialized column types  
- **REST APIs**: Serialization utilities

---

## 🔧 Tests & Coverage

```bash
tox
```

```bash
coverage html && open htmlcov/index.html
```

---

## 📖 Requirements

- Python 3.9 or higher
- (Optional) `tzdata` if using timezones in systems without a local zoneinfo database

---

## 📝 License

MIT © 2025 — Rodrigo Ezequiel Roldán  
[View full license](https://github.com/roldriel/eones/blob/master/LICENSE.md)
