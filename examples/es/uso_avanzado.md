# Uso Avanzado de Eones

Este archivo contiene ejemplos avanzados de manipulación de fechas y horas con Eones.

## Manipulación Avanzada de Fechas

### Truncamiento y Redondeo

```python
fecha = Eones("2024-06-15 14:30:45")

# Truncar al inicio de diferentes unidades
fecha.floor("day")     # 2024-06-15 00:00:00
fecha.floor("month")   # 2024-06-01 00:00:00
fecha.floor("year")    # 2024-01-01 00:00:00
fecha.floor("hour")    # 2024-06-15 14:00:00

# Avanzar al final de diferentes unidades
fecha.ceil("day")      # 2024-06-15 23:59:59
fecha.ceil("month")    # 2024-06-30 23:59:59
fecha.ceil("year")     # 2024-12-31 23:59:59

# Redondear a la unidad más cercana
fecha.round("hour")    # Redondea a la hora más cercana
fecha.round("day")     # Redondea al día más cercana
```

### Inicio y Final de Períodos

```python
fecha = Eones("2024-06-15 14:30:45")

# Ir al inicio de diferentes períodos
fecha.start_of("day")     # 2024-06-15 00:00:00
fecha.start_of("week")    # Lunes de esa semana
fecha.start_of("month")   # 2024-06-01 00:00:00
fecha.start_of("year")    # 2024-01-01 00:00:00

# Ir al final de diferentes períodos
fecha.end_of("day")       # 2024-06-15 23:59:59
fecha.end_of("week")      # Domingo de esa semana
fecha.end_of("month")     # 2024-06-30 23:59:59
fecha.end_of("year")      # 2024-12-31 23:59:59
```

### Reemplazo de Componentes

```python
fecha = Eones("2024-06-15 14:30:45")

# Cambiar componentes específicos
fecha.replace(day=1)           # Cambiar al día 1 del mes
fecha.replace(month=12)        # Cambiar a diciembre
fecha.replace(year=2025)       # Cambiar a 2025
fecha.replace(hour=0, minute=0, second=0)  # Medianoche

print(fecha.format("%Y-%m-%d %H:%M:%S"))
```

## Comparaciones y Validaciones

### Comparaciones entre Fechas

```python
fecha1 = Eones("2024-01-01")
fecha2 = Eones("2024-12-31")
fecha3 = Eones("2024-06-15")

# Verificar si una fecha está entre otras dos
esta_entre = fecha3.is_between(fecha1, fecha2)
print(esta_entre)  # True

# Verificar si están en la misma semana
misma_semana = fecha1.is_same_week(fecha2)
print(misma_semana)  # False

# Verificar si están en el mismo mes/año
mismo_mes = fecha1.is_within(fecha3, check_month=True)
mismo_año = fecha1.is_within(fecha3, check_month=False)
```

### Próximos Días de la Semana

```python
fecha = Eones("2024-06-15")  # Supongamos que es sábado

# Encontrar el próximo lunes (0=Lunes, 6=Domingo)
proximo_lunes = fecha.next_weekday(0)
print(proximo_lunes.format("%Y-%m-%d"))  # Fecha del próximo lunes

# Próximo viernes
proximo_viernes = fecha.next_weekday(4)
print(proximo_viernes.format("%Y-%m-%d"))
```

## Rangos de Fechas

### Obtener rangos de períodos

```python
fecha = Eones("2024-06-15")

# Obtener rangos de diferentes períodos
rango_dia = fecha.range("day")      # (inicio_día, fin_día)
rango_mes = fecha.range("month")    # (inicio_mes, fin_mes)
rango_año = fecha.range("year")     # (inicio_año, fin_año)

# Los rangos devuelven tuplas de datetime
inicio, fin = rango_mes
print(f"Mes: desde {inicio} hasta {fin}")
```

## Métodos Adicionales de la Clase Date

### Navegación por Días de la Semana

```python
fecha = Eones("2024-06-15")  # Supongamos que es sábado

# Encontrar el próximo día específico de la semana
proximo_lunes = fecha.next_weekday(0)    # 0=Lunes, 1=Martes, ..., 6=Domingo
proximo_viernes = fecha.next_weekday(4)

# Encontrar el día anterior específico de la semana
anterior_miercoles = fecha.previous_weekday(2)

print(proximo_lunes.format("%Y-%m-%d"))     # Fecha del próximo lunes
print(anterior_miercoles.format("%Y-%m-%d")) # Fecha del miércoles anterior
```

### Conversión a Diccionario

```python
fecha = Eones("2024-06-15 14:30:45")

# Convertir a diccionario con todos los componentes
dict_fecha = fecha.to_dict()
print(dict_fecha)
# {
#     'year': 2024,
#     'month': 6,
#     'day': 15,
#     'hour': 14,
#     'minute': 30,
#     'second': 45,
#     'microsecond': 0,
#     'timezone': 'UTC'
# }
```

### Rangos de Períodos Específicos

```python
fecha = Eones("2024-06-15")

# Obtener rangos específicos usando la clase Range
rango_trimestre = fecha.quarter_range()  # Inicio y fin del trimestre actual
rango_semana_iso = fecha.week_range()    # Semana ISO (lunes a domingo)

# Los rangos devuelven tuplas de datetime
inicio_trimestre, fin_trimestre = rango_trimestre
print(f"Trimestre: {inicio_trimestre} - {fin_trimestre}")
```