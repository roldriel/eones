# Casos de Uso Comunes con Eones

Este archivo contiene ejemplos prácticos de uso de Eones en situaciones del mundo real.

## 1. Calcular Edad

```python
nacimiento = Eones("1990-05-15")
hoy = Eones()

edad = hoy.difference(nacimiento, unit="years")
print(f"Edad: {edad.total_months // 12} años")
```

## 2. Fechas de Vencimiento

```python
hoy = Eones()
vencimiento = Eones(hoy)
vencimiento.add(days=30)  # Vence en 30 días

print(f"Vence el: {vencimiento.format('%d/%m/%Y')}")
print(f"Tiempo restante: {vencimiento.diff_for_humans(locale='es')}")
```

## 3. Reportes Mensuales

```python
fecha_reporte = Eones("2024-06-15")

# Obtener el rango completo del mes
inicio_mes, fin_mes = fecha_reporte.range("month")

print(f"Reporte del mes: {inicio_mes.strftime('%B %Y')}")
print(f"Desde: {inicio_mes.strftime('%d/%m/%Y')}")
print(f"Hasta: {fin_mes.strftime('%d/%m/%Y')}")
```

## 4. Horarios de Trabajo

```python
# Encontrar el próximo lunes para una reunión
hoy = Eones()
proximo_lunes = hoy.next_weekday(0)  # 0 = Lunes

# Establecer hora de reunión
reunion = Eones(proximo_lunes)
reunion.replace(hour=9, minute=0)  # 9:00 AM

print(f"Próxima reunión: {reunion.format('%A %d de %B a las %H:%M')}")
```

## 5. Validación de Facturas

```python
# Caso 1: Validar si una factura está dentro del mes actual
factura_fecha = Eones("2025-06-08")
actual = Eones("2025-06-15")
if actual.is_within(factura_fecha):
    print("La factura corresponde al mes actual")
```

## 6. Cálculo de Días Restantes

```python
# Caso 2: Calcular cuántos días faltan para el vencimiento
vencimiento = Eones("2025-06-20")
hoy = Eones("2025-06-15")
dias_restantes = hoy.difference(vencimiento, unit="days")
print("Días hasta el vencimiento:", dias_restantes)
```

## 7. Detección de Trimestre Fiscal

```python
# Caso 3: Detectar si una fecha es el inicio de trimestre fiscal
fecha = Eones("2025-07-01")
if fecha.format("%m-%d") in ["01-01", "04-01", "07-01", "10-01"]:
    print("Inicio de trimestre fiscal")
```

## 8. Reporte de Período

```python
# Caso 4: Generar un reporte desde el inicio del mes hasta hoy
hoy = Eones("2025-06-18")
inicio_mes, _ = hoy.range("month")
print("Reporte del:", inicio_mes.date(), "al", hoy.now().to_datetime().date())
```

## 9. Próxima Fecha de Corte

```python
# Caso 5: Estimar próxima fecha de corte semanal (lunes)
hoy = Eones("2025-06-18")
corte = hoy.next_weekday(0)
print("Próximo lunes:", corte.to_datetime().strftime("%Y-%m-%d"))
```

## 10. Calendario Laboral

```python
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
```

## 11. Calcular Próximos Días Laborables

```python
# Calcular próximos 5 días laborables
actual = Eones("2025-05-01")
proximos = []

while len(proximos) < 5:
    actual.add(days=1)
    dt = actual.now().to_datetime()
    if dt.weekday() < 5 and actual.format("%Y-%m-%d") not in feriados:
        proximos.append(actual.format("%Y-%m-%d"))

print("Próximos 5 días laborables:", proximos)
```

## 12. Formateo para APIs

```python
# Serialización para APIs REST
def fecha_para_api(fecha):
    return {
        "fecha": format_date(fecha, "%Y-%m-%d"),
        "fecha_legible": format_date(fecha, "%d de %B de %Y"),
        "timestamp": fecha.timestamp()
    }
```

## 13. Almacenamiento en Base de Datos

```python
# Almacenamiento en base de datos
def guardar_evento(nombre, fecha, duracion):
    return {
        "nombre": nombre,
        "fecha_iso": format_date(fecha, "%Y-%m-%dT%H:%M:%S%z"),
        "duracion_iso": format_duration(duracion)
    }
```

## 14. Logs Estructurados

```python
import logging

# Logs estructurados
def log_evento(evento, fecha):
    logging.info(f"Evento '{evento}' programado para {format_date(fecha, '%Y-%m-%d %H:%M')}")
```