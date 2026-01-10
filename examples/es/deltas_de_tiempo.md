# ⏱️ Deltas de Tiempo

Eones implementa un sistema sofisticado de deltas con **arquitectura dual** que separa claramente los intervalos de tiempo en dos categorías.

## Arquitectura Dual de Deltas

1. **`DeltaCalendar`**: Para intervalos basados en calendario (años, meses, días)
2. **`DeltaDuration`**: Para intervalos basados en duración absoluta (días, horas, minutos, segundos)

## Clase `Delta` Principal

La clase `Delta` principal actúa como una fachada que combina ambos tipos:

```python
from eones.delta import Delta

# Los deltas se crean automáticamente al calcular diferencias
fecha1 = Eones("2024-01-01")
fecha2 = Eones("2024-03-15")

delta = fecha2.difference(fecha1)
print(delta)  # Muestra la diferencia en formato legible

# Los deltas pueden aplicarse a fechas
fecha_nueva = fecha1.add(months=2, days=14)  # Equivalente al delta anterior
```

### Métodos Principales de `Delta`

```python
# Crear deltas
delta = Delta(years=1, months=2, days=10, hours=5, minutes=30)

# Desde timedelta estándar
from datetime import timedelta
td = timedelta(days=3, seconds=3600)
delta = Delta.from_timedelta(td)

# Desde formato ISO 8601
delta = Delta.from_iso("P1Y2M10DT3H30M")
print(delta.to_iso())  # "P1Y2M10DT3H30M"

# Conversiones
print(delta.total_seconds())  # Solo componentes de duración
print(delta.total_months())   # 12 * años + meses

# Operaciones
delta1 = Delta(days=5)
delta2 = Delta(days=2)
resultado = delta1 - delta2  # Delta(days=3)
```

## `DeltaCalendar` - Intervalos de Calendario

Maneja intervalos que dependen de la estructura del calendario (años, meses, días):

```python
from eones.core.delta_calendar import DeltaCalendar
from eones.date import Date

# Crear delta de calendario
dc = DeltaCalendar(years=1, months=2, days=10)

# Aplicar a una fecha (maneja automáticamente límites de mes)
d = Date(2024, 1, 31)  # 31 de enero
new_date = dc.apply(d)  # Suma 1 mes
print(new_date.to_string())  # "2024-02-29" (maneja año bisiesto)

# Casos especiales de fin de mes
d_fin_mes = Date(2024, 1, 31)
dc_un_mes = DeltaCalendar(months=1)
resultado = dc_un_mes.apply(d_fin_mes)
print(resultado.to_string())  # "2024-02-29" (no "2024-02-31")

# Invertir delta
dc_negativo = dc.invert()
print(dc_negativo.years, dc_negativo.months)  # -1, -2

# Operaciones
dc1 = DeltaCalendar(months=3)
dc2 = DeltaCalendar(months=1)
resultado = dc1 - dc2  # DeltaCalendar(months=2)
```

## `DeltaDuration` - Intervalos de Duración

Maneja intervalos de tiempo absolutos que no dependen del calendario:

```python
from eones.core.delta_duration import DeltaDuration
from eones.date import Date

# Crear delta de duración
dd = DeltaDuration(days=2, hours=3, minutes=30, seconds=45)

# Aplicar a una fecha
d = Date.from_string("2024-06-15T10:00:00")
new_date = dd.apply(d)
print(new_date.to_string("%Y-%m-%d %H:%M:%S"))  # "2024-06-17 13:30:45"

# Conversión a timedelta estándar
td = dd.to_timedelta()
print(td)  # "2 days, 3:30:45"

# Invertir delta
dd_negativo = dd.invert()
print(dd_negativo.hours)  # -3

# Operaciones
dd1 = DeltaDuration(hours=5)
dd2 = DeltaDuration(hours=2)
resultado = dd1 - dd2  # DeltaDuration(hours=3)
```

## Cuándo Usar Cada Tipo

**Usa `DeltaCalendar` cuando:**
- Trabajas con meses y años ("el próximo mes", "dentro de 2 años")
- Necesitas respetar límites de calendario (fin de mes, años bisiestos)
- Realizas cálculos de fechas de vencimiento o aniversarios

**Usa `DeltaDuration` cuando:**
- Trabajas con intervalos de tiempo precisos ("en 2 horas y 30 minutos")
- Necesitas duración absoluta independiente del calendario
- Realizas cálculos de tiempo transcurrido o timeouts

**Usa `Delta` principal cuando:**
- Necesitas combinar ambos tipos de intervalos
- Quieres la interfaz más simple y completa
- Trabajas con diferencias calculadas automáticamente

## Ejemplos Prácticos

### Vencimiento Mensual

```python
# Vencimiento mensual (usa DeltaCalendar)
vencimiento = Date(2024, 1, 31)
proximo_vencimiento = DeltaCalendar(months=1).apply(vencimiento)
print(proximo_vencimiento)  # 2024-02-29 (no 2024-02-31)
```

### Timeout de Sesión

```python
# Timeout de sesión (usa DeltaDuration)
inicio_sesion = Date.now()
timeout = DeltaDuration(hours=2)
vence_sesion = timeout.apply(inicio_sesion)
print(f"Sesión vence: {vence_sesion.format('%H:%M')}")
```

### Recordatorio Complejo

```python
# Recordatorio complejo (usa Delta combinado)
recordatorio = Delta(months=1, hours=2)  # Un mes y 2 horas después
fecha_recordatorio = recordatorio.apply(Date.now())
```