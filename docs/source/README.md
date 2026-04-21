<p align="center">
  <img src="eones.png" alt="Eones" width="600">
</p>

> Compatible with Python 3.9+ · No external dependencies · Portable and lightweight

---

![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![PyPI](https://img.shields.io/pypi/v/eones?style=for-the-badge)
![Pylint](https://img.shields.io/badge/pylint-10.00-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-97%25-red?style=for-the-badge)

---

## 🚀 TL;DR

```python
from eones import Eones
# 1.3M ops/sec - The fastest semantic datetime in Python
now = Eones() 
next_month = now.add(months=1)
print(next_month.format("%Y-%m-%d"))
```

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
pip install eones
```

### Timezone support (Optional)
If you're working on Windows or in environments without native zoneinfo data, install the timezone extra:

```bash
pip install "eones[tz]"
```

---

## 🧪 Basic Example

```python
from eones import Eones

e = Eones("2025-06-15")

print(e.add(months=1, days=3))                       # → Eones(date=2025-07-18T00:00:00+00:00, tz='UTC')
print(e.format("%Y-%m-%d"))                          # → 2025-07-18
print(e.diff_for_humans("2025-06-10"))               # → in 1 month
print(e.diff_for_humans("2025-06-20", locale="es"))  # → en 4 semanas
```

---

## 🔍 Key Features

- ✅ **Zero external dependencies**: Pure Python (Python 3.9+)
- ✅ **Intuitive interface**: Simple, semantically rich and easy-to-use API
- ✅ **Modern timezone support**: Robust handling with `zoneinfo` (not `pytz`)
- ✅ **Flexible parsing**: Accepts multiple date formats automatically, including ISO 8601 with timezone offsets
- ✅ **Advanced temporal operations**: Deltas, ranges and semantic comparisons
- ✅ **Modular architecture**: Clear separation between `Date`, `Delta`, `Range` and utilities
- ✅ **Holiday Calendars**: 7 national calendars (AR, US, FR, DE, ES, JP, AU) with custom calendar support
- ✅ **Business Day Logic**: `is_business_day()`, `add_business_days()`, `count_business_days()` and more
- ✅ **Localization**: 5 languages (en, es, fr, de, ja) with locale-aware date formatting
- ✅ **Humanization**: Converts time differences to readable text in any supported locale
- ✅ **Complete type hinting**: Fully typed following PEP 561
- ✅ **Interoperability**: Compatible with Python's standard `datetime`

### Business Days & Holidays

```python
e = Eones("2026-05-25", locale="es", calendar="America/Argentina")

e.is_holiday()                          # True (Día de la Revolución de Mayo)
e.holiday_name()                        # "Día de la Revolución de Mayo"
e.is_business_day()                     # False
e.next_business_day()                   # 2026-05-26

# Locale-aware formatting
e.format_locale("DD de MMMM de YYYY")  # "25 de mayo de 2026"

# Static business day metrics
Eones.count_business_days("2026-01-01", "2026-01-31")  # 22
Eones.available_calendars()             # ['America/Argentina', 'America/US', ...]
```

### Localization & Error Handling

Eones supports 5 locales out of the box: `en`, `es`, `fr`, `de`, `ja`. You can add more
by creating a file in `eones/locales/`. See the [Locale Guide](docs/LOCALE_GUIDE.md).

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

---

## 📚 Documentation & Examples

Comprehensive examples and documentation are available:

### 📖 Core Examples
- **[Quick Start](https://github.com/roldriel/eones/blob/master/docs/source/examples/quick_start.md)** - Library import, date creation, formatting, basic operations
- **[Advanced Patterns](https://github.com/roldriel/eones/blob/master/docs/source/examples/advanced_patterns.md)** - Truncation, rounding, period ranges, comparisons
- **[Time Deltas](https://github.com/roldriel/eones/blob/master/docs/source/examples/time_deltas.md)** - Dual delta architecture, calendar vs duration intervals
- **[Real World Scenarios](https://github.com/roldriel/eones/blob/master/docs/source/examples/real_world_scenarios.md)** - Real-world examples: age calculation, billing cycles, reports
- **[Error Handling](https://github.com/roldriel/eones/blob/master/docs/source/examples/error_handling.md)** - Exception hierarchy, safe date creation, validation
- **[Formatting & Serialization](https://github.com/roldriel/eones/blob/master/docs/source/examples/formatting_serialization.md)** - ISO 8601, JSON export/import, API integration
- **[Regional Configuration](https://github.com/roldriel/eones/blob/master/docs/source/examples/regional_configuration.md)** - First day of week configuration, ISO vs US standards, weekend detection
- **[Business Calendar](https://github.com/roldriel/eones/blob/master/examples/business_calendar.md)** - Holiday calendars, business day operations, custom calendars
- **[Locale Formatting](https://github.com/roldriel/eones/blob/master/examples/locale_formatting.md)** - Localized date formatting with `format_locale()`, multi-language support

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
