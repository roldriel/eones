# examples/basic_usage.py
from datetime import datetime

from zilean import Zilean

# 1. Crear fechas desde distintos formatos
z1 = Zilean("2025-06-15")
z2 = Zilean({"year": 2025, "month": 6, "day": 15})
z3 = Zilean(datetime(2025, 6, 15))
print("Format date:", z1.format("%Y-%m-%d"))

# 2. Agregar tiempo
z1.add(years=1, months=2, days=10)
print("After add:", z1.format("%Y-%m-%d"))

# 3. Diferencias
base = Zilean("2025-01-01")
print("Diff days:", base.difference("2025-01-04", unit="days"))
print("Diff months:", base.difference("2025-03-01", unit="months"))
print("Diff years:", base.difference("2027-01-01", unit="years"))

# 4. Comparaciones
z = Zilean("2025-06-10")
print("Is within same month:", z.is_within("2025-06-01"))
print("Is same year:", z.is_within("2025-01-01", check_month=False))

# 5. Rango mensual
start, end = z.range("month")
print("Month range:", start, "to", end)

# 6. Próximo lunes desde una fecha
monday = z.next_weekday(0)
print("Next Monday:", monday.to_datetime())
