# Uso Básico de Eones

Este archivo contiene ejemplos básicos para comenzar a usar la librería Eones.

## Importación

```python
from eones import Eones
```

## Creación de Fechas

### Diferentes formas de crear fechas

```python
# Fecha actual
fecha_actual = Eones()

# Desde string (múltiples formatos soportados)
fecha1 = Eones("2024-12-25")
fecha2 = Eones("25/12/2024")
fecha3 = Eones("25-12-2024")
fecha4 = Eones("2024-12-25 15:30:00")

# Desde diccionario
fecha5 = Eones({"year": 2024, "month": 12, "day": 25, "hour": 15})

# Desde datetime de Python
from datetime import datetime
fecha6 = Eones(datetime.now())

# Desde cadenas ISO 8601 (con soporte de zona horaria)
fecha7 = Eones("2024-12-25T15:30:00Z")           # UTC
fecha8 = Eones("2024-12-25T15:30:00+03:00")      # Con offset positivo
fecha9 = Eones("2024-12-25T15:30:00-05:00")      # Con offset negativo
fecha10 = Eones("2024-12-25T15:30:00.123456+02:30")  # Con microsegundos y offset

# Con zona horaria específica
fecha_madrid = Eones("2024-12-25", tz="Europe/Madrid")
fecha_mexico = Eones("2024-12-25", tz="America/Mexico_City")
```

## Formateo de Fechas

### Diferentes formatos de salida

```python
fecha = Eones("2024-12-25 15:30:00")

# Diferentes formatos de salida
print(fecha.format("%Y-%m-%d"))           # 2024-12-25
print(fecha.format("%d/%m/%Y"))           # 25/12/2024
print(fecha.format("%d de %B de %Y"))     # 25 de December de 2024
print(fecha.format("%H:%M:%S"))           # 15:30:00
```

## Suma y Resta de Tiempo

### Agregar tiempo a una fecha

```python
fecha = Eones("2024-01-15")

# Agregar tiempo
fecha.add(days=10)          # Suma 10 días
fecha.add(months=2)         # Suma 2 meses
fecha.add(years=1, days=5)  # Suma 1 año y 5 días
fecha.add(hours=3, minutes=30)  # Suma 3 horas y 30 minutos

print(fecha.format("%Y-%m-%d %H:%M"))  # Resultado después de las sumas
```

## Diferencias entre Fechas

### Calcular diferencias

```python
fecha1 = Eones("2024-01-01")
fecha2 = Eones("2024-12-31")

# Calcular diferencia
diferencia = fecha2.difference(fecha1)
print(diferencia)  # Muestra la diferencia en formato Delta

# Diferencia en unidades específicas
diferencia_dias = fecha2.difference(fecha1, unit="days")
diferencia_meses = fecha2.difference(fecha1, unit="months")

# Diferencia legible para humanos
print(fecha2.diff_for_humans(fecha1))  # "11 months ago" (en inglés)
print(fecha2.diff_for_humans(fecha1, locale="es"))  # "hace 11 meses" (en español)
```

## Parsing Personalizado

### Usar formatos personalizados

```python
# Usar formatos personalizados
formatos_personalizados = ["%d-%m-%Y", "%Y/%m/%d"]
fecha = Eones("15-06-2024", formats=formatos_personalizados)

# Agregar formatos adicionales a los predeterminados
fecha = Eones("15-06-2024", additional_formats=["%d-%m-%Y"])
```

## Localización

### Soporte para múltiples idiomas

```python
fecha1 = Eones("2024-01-01")
fecha2 = Eones("2024-01-15")

# En inglés (predeterminado)
print(fecha2.diff_for_humans(fecha1))  # "2 weeks ago"

# En español
print(fecha2.diff_for_humans(fecha1, locale="es"))  # "hace 2 semanas"
```