# 🌍 Configuración Regional

Eones v1.4.0 introduce la capacidad de configurar el primer día de la semana para adaptarse a diferentes estándares culturales y regionales.

## Configuración Global

Por defecto, Eones utiliza el estándar ISO donde el lunes es el primer día de la semana (valor 0). Puedes cambiar esto modificando la constante `FIRST_DAY_OF_WEEK`:

```python
from eones import constants

# Configurar para estándar ISO (lunes primero) - por defecto
constants.FIRST_DAY_OF_WEEK = 0

# Configurar para estándar US (domingo primero)
constants.FIRST_DAY_OF_WEEK = 6
```

## Impacto en los Métodos

### is_weekend()

El método `is_weekend()` se adapta automáticamente a la configuración:

```python
from eones import Date
from eones import constants
from datetime import datetime

# Crear una fecha de viernes
viernes = Date(datetime(2024, 1, 5))  # Viernes

# Estándar ISO (lunes primero): viernes NO es fin de semana
constants.FIRST_DAY_OF_WEEK = 0
print(f"ISO - Viernes es fin de semana: {viernes.is_weekend()}")  # False

# Estándar US (domingo primero): viernes SÍ es fin de semana
constants.FIRST_DAY_OF_WEEK = 6
print(f"US - Viernes es fin de semana: {viernes.is_weekend()}")   # True
```

### week_range()

El método `week_range()` también acepta un parámetro opcional para especificar el primer día:

```python
from eones import Date, Range
from datetime import datetime

# Martes, 10 de junio de 2025
fecha = Date(datetime(2025, 6, 10))
r = Range(fecha)

# Semana ISO (lunes a domingo)
start_iso, end_iso = r.week_range(first_day_of_week=0)
print(f"Semana ISO: {start_iso.day} al {end_iso.day}")  # 9 al 15

# Semana US (domingo a sábado)
start_us, end_us = r.week_range(first_day_of_week=6)
print(f"Semana US: {start_us.day} al {end_us.day}")    # 8 al 14
```

## Funciones Helper

Eones proporciona funciones helper para convertir entre sistemas de numeración:

```python
from eones.constants import iso_to_us_weekday, us_to_iso_weekday, is_weekend_day

# Convertir de ISO a US
iso_monday = 0  # Lunes en ISO
us_monday = iso_to_us_weekday(iso_monday)
print(f"Lunes ISO ({iso_monday}) = Lunes US ({us_monday})")  # 0 = 1

# Convertir de US a ISO
us_sunday = 0  # Domingo en US
iso_sunday = us_to_iso_weekday(us_sunday)
print(f"Domingo US ({us_sunday}) = Domingo ISO ({iso_sunday})")  # 0 = 6

# Verificar fin de semana con configuración específica
print(f"¿Viernes es fin de semana en ISO? {is_weekend_day(4, 0)}")  # False
print(f"¿Viernes es fin de semana en US? {is_weekend_day(4, 6)}")   # True
```

## Sistemas de Numeración

### ISO (Estándar Internacional)
- 0: Lunes
- 1: Martes
- 2: Miércoles
- 3: Jueves
- 4: Viernes
- 5: Sábado
- 6: Domingo
- **Fin de semana**: Sábado y Domingo

### US (Estándar Estadounidense)
- 0: Domingo
- 1: Lunes
- 2: Martes
- 3: Miércoles
- 4: Jueves
- 5: Viernes
- 6: Sábado
- **Fin de semana**: Viernes y Sábado (en numeración ISO: 4 y 5)

## Casos de Uso

### Aplicaciones Internacionales
```python
# Configurar según la región del usuario
def configurar_semana_por_region(region):
    if region in ['US', 'CA', 'MX']:  # América del Norte
        constants.FIRST_DAY_OF_WEEK = 6  # Domingo primero
    else:  # Europa, Asia, etc.
        constants.FIRST_DAY_OF_WEEK = 0  # Lunes primero
```

### Reportes de Negocio
```python
# Generar reporte semanal adaptado a la cultura local
def generar_reporte_semanal(fecha, region='ISO'):
    r = Range(fecha)
    first_day = 6 if region == 'US' else 0
    start, end = r.week_range(first_day_of_week=first_day)
    
    print(f"Reporte semanal del {start.strftime('%d/%m/%Y')} al {end.strftime('%d/%m/%Y')}")
    return start, end
```

## Notas Importantes

1. **Compatibilidad**: El cambio de `FIRST_DAY_OF_WEEK` afecta globalmente a todos los métodos que dependen de la configuración de semana.

2. **Persistencia**: La configuración se mantiene durante toda la sesión de Python. Para cambios permanentes, considera configurarla al inicio de tu aplicación.

3. **Thread Safety**: Ten cuidado al cambiar la configuración en aplicaciones multi-hilo, ya que afecta globalmente.

4. **Retrocompatibilidad**: Por defecto, Eones mantiene el comportamiento ISO existente, por lo que el código existente seguirá funcionando sin cambios.