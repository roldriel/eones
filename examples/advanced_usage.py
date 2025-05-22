# examples/advanced_usage.py
from datetime import datetime

from eones import Eones

# Caso 1: Validar si una factura está dentro del mes actual
factura_fecha = Eones("2025-06-08")
actual = Eones("2025-06-15")
if actual.is_within(factura_fecha):
    print("La factura corresponde al mes actual")

# Caso 2: Calcular cuántos días faltan para el vencimiento
vencimiento = Eones("2025-06-20")
hoy = Eones("2025-06-15")
dias_restantes = hoy.difference(vencimiento, unit="days")
print("Días hasta el vencimiento:", dias_restantes)

# Caso 3: Detectar si una fecha es el inicio de trimestre fiscal
fecha = Eones("2025-07-01")
if fecha.format("%m-%d") in ["01-01", "04-01", "07-01", "10-01"]:
    print("Inicio de trimestre fiscal")

# Caso 4: Generar un reporte desde el inicio del mes hasta hoy
hoy = Eones("2025-06-18")
inicio_mes, _ = hoy.range("month")
print("Reporte del:", inicio_mes.date(), "al", hoy.now().to_datetime().date())

# Caso 5: Estimar próxima fecha de corte semanal (lunes)
corte = hoy.next_weekday(0)
print("Próximo lunes:", corte.to_datetime().strftime("%Y-%m-%d"))
