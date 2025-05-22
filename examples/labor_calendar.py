# examples/labor_calendar.py
from datetime import datetime

from eones import Eones

# Lista de feriados (puede venir de una base de datos externa)
feriados = [
    "2025-01-01",  # Año Nuevo
    "2025-05-01",  # Día del Trabajador
    "2025-12-25",  # Navidad
]

# Verificar si una fecha es laborable
fecha = Eones("2025-05-01")

is_weekend = fecha.now().to_datetime().weekday() >= 5  # 5 = Sábado, 6 = Domingo
is_feriado = fecha.format("%Y-%m-%d") in feriados

if is_weekend or is_feriado:
    print("No laborable")
else:
    print("Laborable")

# Calcular próximos 5 días laborables
actual = Eones("2025-05-01")
proximos = []

while len(proximos) < 5:
    actual.add(days=1)
    dt = actual.now().to_datetime()
    if dt.weekday() < 5 and actual.format("%Y-%m-%d") not in feriados:
        proximos.append(actual.format("%Y-%m-%d"))

print("Próximos 5 días laborables:", proximos)
