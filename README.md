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

> *“That is not dead which can eternal lie, and with strange aeons even death may die.”*  
> — *Abdul Alhazred*, Necronomicon

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

- ✅ Automatic parsing for `str`, `dict`, `datetime`, `Eones`
- ✅ Add/subtract days, months, years, minutes, seconds
- ✅ Date comparison (same week, within year, between ranges)
- ✅ Full day/month/year ranges
- ✅ Truncation and rounding by unit
- ✅ Full support for `ZoneInfo` (PEP 615)
- ✅ Zero external dependencies
- ✅ Conversion to `datetime`, `date`, and native types
- ✅ Human-friendly differences via `diff_for_humans` with locale support

You can add more languages by creating a new file in `eones/locales/` with the
translations for your locale. For example, `fr.py` for French.

---

## 🧾 Comparison with other libraries

| Feature                                 | Eones | Pendulum | Arrow | Delorean | dateutil | pytz |
|-----------------------------------------|:-----:|:--------:|:-----:|:--------:|:--------:|:----:|
| Modern, consistent API                  | ✅    | ✅        | ✅    | ⚠️        | ❌        | ❌   |
| Date arithmetic (add/subtract)          | ✅    | ✅        | ✅    | ✅        | ❌        | ❌   |
| Flexible parsing (string, dict, dt)     | ✅    | ✅        | ✅    | ⚠️        | ✅        | ❌   |
| Native timezone support                 | ✅    | ✅        | ✅    | ✅        | ⚠️        | ✅   |
| No external dependencies                | ✅    | ❌        | ❌    | ❌        | ❌        | ❌   |
| Coverage tested ≥ 97%                   | ✅    | ❓        | ❓    | ❌        | ❌        | ❌   |
| Can replace native `datetime` directly  | ✅    | ✅        | ✅    | ❌        | ❌        | ❌   |
| Permissive license (MIT / BSD)          | ✅    | ✅        | ✅    | ✅        | ✅        | ✅   |
| Actively maintained                     | ✅    | ✅        | ✅    | ❌        | ✅        | ⚠️   |

---

## 📚 Advanced Examples

You can find more usage examples in:

- [examples/basic_usage.py](https://github.com/roldriel/eones/blob/master/examples/basic_usage.py)
- [examples/advanced_usage.py](https://github.com/roldriel/eones/blob/master/examples/advanced_usage.py)
- [examples/labor_calendar.py](https://github.com/roldriel/eones/blob/master/examples/labor_calendar.py)

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
