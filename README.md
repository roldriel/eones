# Eones
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-manual-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-97%25-blue?style=for-the-badge)
![Tox](https://img.shields.io/badge/Tested%20with-tox-yellowgreen?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/eones?style=for-the-badge)
![ChatGPT](https://img.shields.io/badge/ChatGPT-Collaborator-lightgrey?style=for-the-badge&logo=openai)

---

> Compatible with Python 3.8+ · No external dependencies · Portable and lightweight

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
z.add(months=1, days=3)

print(z.format("%Y-%m-%d"))  # → 2025-07-18
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

- [examples/basic_usage.py](examples/basic_usage.py)
- [examples/advanced_usage.py](examples/advanced_usage.py)
- [examples/labor_calendar.py](examples/labor_calendar.py)

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

- Python 3.8 or higher
- (Optional) `tzdata` if using timezones in systems without a local zoneinfo database

---

## 📝 License

MIT © 2025 — Rodrigo Ezequiel Roldán  
[View full license](LICENSE.md)
