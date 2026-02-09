# ✨ What is Eones?

![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![PyPI](https://img.shields.io/pypi/v/eones?style=for-the-badge)
![Pylint](https://img.shields.io/badge/pylint-10.00-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-100%25-red?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-manual-green?style=for-the-badge)
![Tox](https://img.shields.io/badge/Tested%20tox-yellowgreen?style=for-the-badge)

---

> Compatible with Python 3.9+ · No external dependencies · Portable and lightweight

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
