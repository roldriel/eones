# 🎨 Formateo y Serialización

Eones incluye utilidades especializadas para formateo y serialización de objetos `Date` y `Delta`.

## Formateo de Fechas

### Formateo Básico

```python
from eones.formats import format_date
from eones.date import Date

# Formateo básico
d = Date(2024, 6, 15)
print(format_date(d))  # "2024-06-15" (formato por defecto)
print(format_date(d, "%d/%m/%Y"))  # "15/06/2024"
```

### Formateo con Zona Horaria

```python
# Formateo con zona horaria
d_madrid = Date(2024, 6, 15, tz="Europe/Madrid")
print(format_date(d_madrid, "%Y-%m-%d %H:%M %Z"))  # "2024-06-15 00:00 CEST"

# Usado internamente por Date.to_string()
print(d.to_string("%A, %d de %B de %Y"))  # Usa format_date internamente
```

## Serialización de Duraciones

### Serialización ISO 8601

```python
from eones.formats import format_duration
from eones.delta import Delta

# Serialización ISO 8601
delta = Delta(years=1, months=2, days=3, hours=4, minutes=30)
print(format_duration(delta))  # "P1Y2M3DT4H30M"
```

### Casos Especiales de Duración

```python
# Casos especiales
delta_solo_tiempo = Delta(hours=2, minutes=15)
print(format_duration(delta_solo_tiempo))  # "PT2H15M"

delta_solo_fecha = Delta(years=1, days=10)
print(format_duration(delta_solo_fecha))  # "P1Y10D"

# Usado internamente por Delta.to_iso()
print(delta.to_iso())  # Usa format_duration internamente
```

## Casos de Uso Comunes

### Serialización para APIs REST

```python
def fecha_para_api(fecha):
    """Convierte una fecha para uso en APIs REST."""
    return {
        "fecha": format_date(fecha, "%Y-%m-%d"),
        "fecha_legible": format_date(fecha, "%d de %B de %Y"),
        "timestamp": fecha.timestamp()
    }

# Ejemplo de uso
fecha = Date(2024, 12, 25)
api_data = fecha_para_api(fecha)
print(api_data)
# {
#     "fecha": "2024-12-25",
#     "fecha_legible": "25 de December de 2024",
#     "timestamp": 1735084800.0
# }
```

### Almacenamiento en Base de Datos

```python
def guardar_evento(nombre, fecha, duracion):
    """Prepara datos de evento para almacenamiento en BD."""
    return {
        "nombre": nombre,
        "fecha_iso": format_date(fecha, "%Y-%m-%dT%H:%M:%S%z"),
        "duracion_iso": format_duration(duracion)
    }

# Ejemplo de uso
fecha_evento = Date(2024, 6, 15, 14, 30)
duracion_evento = Delta(hours=2, minutes=30)

evento_data = guardar_evento("Reunión de equipo", fecha_evento, duracion_evento)
print(evento_data)
# {
#     "nombre": "Reunión de equipo",
#     "fecha_iso": "2024-06-15T14:30:00+00:00",
#     "duracion_iso": "PT2H30M"
# }
```

### Logs Estructurados

```python
import logging

def log_evento(evento, fecha):
    """Registra un evento con formato de fecha legible."""
    fecha_formateada = format_date(fecha, '%Y-%m-%d %H:%M')
    logging.info(f"Evento '{evento}' programado para {fecha_formateada}")

# Ejemplo de uso
fecha_log = Date(2024, 6, 15, 10, 30)
log_evento("Backup automático", fecha_log)
# INFO:root:Evento 'Backup automático' programado para 2024-06-15 10:30
```

### Exportación a JSON

```python
import json
from datetime import datetime

class EonesJSONEncoder(json.JSONEncoder):
    """Encoder JSON personalizado para objetos Eones."""
    
    def default(self, obj):
        if isinstance(obj, Date):
            return {
                "_type": "Date",
                "iso": format_date(obj, "%Y-%m-%dT%H:%M:%S%z"),
                "readable": format_date(obj, "%d de %B de %Y a las %H:%M")
            }
        elif isinstance(obj, Delta):
            return {
                "_type": "Delta",
                "iso": format_duration(obj),
                "components": {
                    "years": obj.years,
                    "months": obj.months,
                    "days": obj.days,
                    "hours": obj.hours,
                    "minutes": obj.minutes,
                    "seconds": obj.seconds
                }
            }
        return super().default(obj)

# Ejemplo de uso
data = {
    "evento": "Conferencia",
    "fecha": Date(2024, 9, 15, 9, 0),
    "duracion": Delta(hours=8, minutes=30)
}

json_str = json.dumps(data, cls=EonesJSONEncoder, indent=2)
print(json_str)
```

### Importación desde JSON

```python
def decode_eones_json(dct):
    """Decodifica objetos Eones desde JSON."""
    if "_type" in dct:
        if dct["_type"] == "Date":
            return Date.from_string(dct["iso"])
        elif dct["_type"] == "Delta":
            return Delta.from_iso(dct["iso"])
    return dct

# Ejemplo de uso
json_data = '''
{
  "evento": "Conferencia",
  "fecha": {
    "_type": "Date",
    "iso": "2024-09-15T09:00:00+00:00"
  },
  "duracion": {
    "_type": "Delta",
    "iso": "PT8H30M"
  }
}
'''

data = json.loads(json_data, object_hook=decode_eones_json)
print(f"Evento: {data['evento']}")
print(f"Fecha: {data['fecha'].format('%d/%m/%Y %H:%M')}")
print(f"Duración: {data['duracion'].total_seconds() / 3600} horas")
```

### Formateo para Diferentes Locales

```python
def formatear_fecha_locale(fecha, locale="es"):
    """Formatea fecha según el locale especificado."""
    formatos = {
        "es": "%d de %B de %Y",
        "en": "%B %d, %Y",
        "fr": "%d %B %Y",
        "de": "%d. %B %Y"
    }
    
    formato = formatos.get(locale, formatos["en"])
    return format_date(fecha, formato)

# Ejemplo de uso
fecha = Date(2024, 6, 15)
print(formatear_fecha_locale(fecha, "es"))  # "15 de June de 2024"
print(formatear_fecha_locale(fecha, "en"))  # "June 15, 2024"
print(formatear_fecha_locale(fecha, "fr"))  # "15 June 2024"
```

### Validación de Formatos

```python
def validar_formato_fecha(fecha_str, formato):
    """Valida si una fecha string coincide con el formato esperado."""
    try:
        fecha = Date.from_string(fecha_str)
        fecha_formateada = format_date(fecha, formato)
        return fecha_str == fecha_formateada
    except Exception:
        return False

# Ejemplo de uso
print(validar_formato_fecha("2024-06-15", "%Y-%m-%d"))  # True
print(validar_formato_fecha("15/06/2024", "%Y-%m-%d"))  # False
```