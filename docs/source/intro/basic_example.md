# 🧪 Basic Example

```python
from eones import Eones

e = Eones("2025-06-15")

print(e.add(months=1, days=3))                       # → Eones(date=2025-07-18T00:00:00+00:00, tz='UTC')
print(e.format("%Y-%m-%d"))                          # → 2025-07-18
print(e.diff_for_humans("2025-06-10"))               # → in 1 month
print(e.diff_for_humans("2025-06-20", locale="es"))  # → en 4 semanas
```
