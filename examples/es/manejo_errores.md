# 🛡️ Manejo de Errores

Eones define un sistema robusto de excepciones específicas para diferentes tipos de errores, todas heredando de una clase base común `EonesError`.

## Jerarquía de Excepciones

```python
from eones.errors import (
    EonesError,                    # Excepción base
    InvalidTimezoneError,          # Zona horaria inválida
    InvalidDateFormatError,        # Formato de fecha inválido
    InvalidDurationFormatError     # Formato de duración inválido
)
```

## `EonesError` - Excepción Base

Todas las excepciones personalizadas de Eones heredan de esta clase base:

```python
class EonesError(Exception):
    pass
```

Esto permite capturar cualquier error específico de Eones:

```python
try:
    fecha = Eones("fecha-inválida", tz="Zona/Inexistente")
except EonesError as e:
    print(f"Error de Eones: {e}")
```

## `InvalidTimezoneError`

Se lanza cuando se proporciona una zona horaria no reconocida:

```python
try:
    fecha = Eones("2024-01-01", tz="Zona/Inexistente")
except InvalidTimezoneError as e:
    print(f"Zona horaria inválida: {e}")
    # Usar zona horaria por defecto
    fecha = Eones("2024-01-01")  # UTC por defecto
```

## `InvalidDateFormatError`

Se lanza cuando el string de fecha no puede ser parseado correctamente:

```python
try:
    fecha = Eones("fecha-completamente-inválida")
except InvalidDateFormatError as e:
    print(f"Formato de fecha inválido: {e}")
    # Intentar con formato específico
    fecha = Eones("2024-01-01", formats=["%Y-%m-%d"])
```

## `InvalidDurationFormatError`

Se lanza cuando un string de duración en formato ISO 8601 no es válido:

```python
from eones.delta import Delta

try:
    delta = Delta.from_iso("P1Y2M3D4H5M6S-INVALID")
except InvalidDurationFormatError as e:
    print(f"Formato de duración ISO inválido: {e}")
    # Crear delta manualmente
    delta = Delta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
```

## Manejo Robusto de Errores

### Función de Creación Segura

```python
def crear_fecha_segura(fecha_str, tz_str=None):
    """Crea una fecha de manera segura con manejo de errores."""
    try:
        return Eones(fecha_str, tz=tz_str)
    except InvalidDateFormatError:
        print(f"Formato de fecha inválido: {fecha_str}")
        return None
    except InvalidTimezoneError:
        print(f"Zona horaria inválida: {tz_str}, usando UTC")
        return Eones(fecha_str)  # UTC por defecto
    except EonesError as e:
        print(f"Error general de Eones: {e}")
        return None

# Uso
fecha = crear_fecha_segura("2024-12-25", "Europe/Madrid")
if fecha:
    print(f"Fecha creada: {fecha.format('%Y-%m-%d %Z')}")
```

### Manejo de Múltiples Formatos

```python
def parsear_fecha_flexible(fecha_str):
    """Intenta parsear una fecha con múltiples estrategias."""
    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for formato in formatos:
        try:
            return Eones(fecha_str, formats=[formato])
        except InvalidDateFormatError:
            continue
    
    # Si ningún formato funciona
    raise InvalidDateFormatError(f"No se pudo parsear la fecha: {fecha_str}")

# Uso
try:
    fecha = parsear_fecha_flexible("25/12/2024")
    print(f"Fecha parseada: {fecha.format('%Y-%m-%d')}")
except InvalidDateFormatError as e:
    print(f"Error: {e}")
```

### Validación de Entrada de Usuario

```python
def validar_entrada_usuario(fecha_input, tz_input=None):
    """Valida y procesa entrada de usuario con feedback detallado."""
    errores = []
    
    # Validar fecha
    fecha = None
    try:
        fecha = Eones(fecha_input, tz=tz_input)
    except InvalidDateFormatError:
        errores.append(f"Formato de fecha inválido: '{fecha_input}'")
        errores.append("Formatos válidos: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY")
    except InvalidTimezoneError:
        errores.append(f"Zona horaria inválida: '{tz_input}'")
        errores.append("Ejemplo de zona válida: 'Europe/Madrid', 'America/New_York'")
        # Intentar sin zona horaria
        try:
            fecha = Eones(fecha_input)
            errores.append("Usando UTC como zona horaria por defecto")
        except InvalidDateFormatError:
            errores.append("Tampoco se pudo parsear la fecha sin zona horaria")
    except EonesError as e:
        errores.append(f"Error inesperado: {e}")
    
    return fecha, errores

# Uso
fecha, errores = validar_entrada_usuario("25/12/2024", "Europe/Madrid")
if errores:
    for error in errores:
        print(f"⚠️  {error}")
if fecha:
    print(f"✅ Fecha válida: {fecha.format('%Y-%m-%d %Z')}")
```

### Logging de Errores

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def procesar_fecha_con_log(fecha_str, tz_str=None):
    """Procesa fecha con logging detallado de errores."""
    try:
        fecha = Eones(fecha_str, tz=tz_str)
        logger.info(f"Fecha procesada exitosamente: {fecha.format('%Y-%m-%d %Z')}")
        return fecha
    except InvalidDateFormatError as e:
        logger.error(f"Error de formato de fecha: {e}")
        logger.info(f"Entrada recibida: '{fecha_str}'")
        raise
    except InvalidTimezoneError as e:
        logger.warning(f"Zona horaria inválida: {e}")
        logger.info(f"Reintentando con UTC...")
        return Eones(fecha_str)  # Fallback a UTC
    except EonesError as e:
        logger.error(f"Error inesperado de Eones: {e}")
        raise
```

## Contextos de Uso de las Excepciones

Estas excepciones son utilizadas internamente en:
- **`parser.py`**: Al parsear fechas o duraciones inválidas
- **`Date` y `Delta`**: Al inicializar objetos con datos incorrectos
- **`interface.py`**: Al validar entradas del usuario
- **Métodos de conversión**: Al convertir entre formatos

## Mejores Prácticas

1. **Siempre captura excepciones específicas** antes que la excepción base
2. **Proporciona mensajes de error útiles** al usuario
3. **Implementa fallbacks sensatos** cuando sea posible
4. **Registra errores** para debugging y monitoreo
5. **Valida entradas** antes de procesarlas cuando sea crítico