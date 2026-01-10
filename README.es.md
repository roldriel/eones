# Eones
![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![PyPI](https://img.shields.io/pypi/v/eones?style=for-the-badge)
![Pylint](https://img.shields.io/badge/pylint-10.00-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-100%25-red?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-manual-green?style=for-the-badge)
![Tox](https://img.shields.io/badge/Tested%20tox-yellowgreen?style=for-the-badge)

---

> Compatible con Python 3.9+ · Sin dependencias externas · Portátil y liviana

---

## ✨ ¿Qué es Eones?

Eones es una librería minimalista, sin dependencias externas, para trabajar con fechas y operaciones de tiempo de manera expresiva, clara y poderosa. Inspirada en la semántica natural del lenguaje, permite manipular, comparar y transformar fechas como si fueran entidades vivas.

> *"No está muerto lo que yace eternamente, y con el paso de extraños eones, incluso la muerte puede morir."*  
> — *Abdul Alhazred*, Necronomicón

### Filosofía

> **Eones no es un reemplazo de datetime. Es una capa de razonamiento temporal.**

Eones existe para llenar el vacío entre el `datetime` de bajo nivel de Python y la necesidad de manipulación de fechas semántica y consciente del calendario:

- Usando **solo la librería estándar** (Python 3.9+)
- Proporcionando una **API semánticamente rica y consistente**
- Soportando diseño moderno y consciente de zonas horarias con `zoneinfo`
- Manteniéndose **modular y componible** a través de separación clara de responsabilidades (`Date`, `Delta`, `Range`)

**Eones es para:**
- Desarrolladores que quieren razonar sobre el tiempo semánticamente, no solo manipular timestamps
- Equipos que quieren **cero dependencias externas** para máxima portabilidad
- Proyectos donde **zonas horarias, truncamiento, deltas y rangos** son lógica de dominio central

---

## 📦 Instalación

```bash
pip install "eones"
```

> Si vas a trabajar con zonas horarias en Windows o contenedores:  
> ⚠️ Instala también `tzdata`:
> ```bash
> pip install tzdata
> ```

---

## 🧪 Ejemplo básico

```python
from eones import Eones

z = Eones("2025-06-15")
z.add(months=1, days=3)  # -> agregar 3 días y 1 mes

print(z.format("%Y-%m-%d"))  # → 2025-07-18
print(z.diff_for_humans("2025-06-10"))  # → en 5 días
print(z.diff_for_humans("2025-06-20", locale="es"))  # → hace 5 días
```

---

## 🔍 Características principales

- ✅ **Sin dependencias externas**: Python puro (Python 3.9+)
- ✅ **Interfaz intuitiva**: API simple, semánticamente rica y fácil de usar
- ✅ **Soporte moderno de zonas horarias**: Manejo robusto con `zoneinfo` (no `pytz`)
- ✅ **Parsing flexible**: Acepta múltiples formatos de fecha automáticamente
- ✅ **Operaciones temporales avanzadas**: Deltas, rangos y comparaciones semánticas
- ✅ **Arquitectura modular**: Separación clara entre `Date`, `Delta`, `Range` y utilidades
- ✅ **Localización**: Soporte para múltiples idiomas
- ✅ **Humanización**: Convierte diferencias de tiempo a texto legible
- ✅ **Type hinting completo**: Totalmente tipado siguiendo PEP 561
- ✅ **Interoperabilidad**: Compatible con `datetime` estándar de Python

### Localización y Manejo de Errores

Podés agregar más idiomas creando un archivo en `eones/locales/` con las
traducciones para tu idioma. Por ejemplo, `fr.py` para francés.

Eones muestra excepciones claras derivadas de `EonesError`. Las zonas horarias no válidas generan `InvalidTimezoneError`, mientras que las cadenas no analizables generan `InvalidFormatError`.

---

## 🧾 Comparación con otras librerías

### ¿Por qué no Pendulum o Arrow?

| Característica                          | Eones | Pendulum | Arrow | Delorean | dateutil | pytz |
|-----------------------------------------|:-----:|:--------:|:-----:|:--------:|:--------:|:----:|
| Soporte moderno de zonas horarias       | ✅ (`zoneinfo`) | ❌ (`pytz`) | ❌ (`pytz`) | ✅ | ⚠️ | ✅ |
| Dependencias externas                   | ✅ Ninguna | ❌ Sí | ❌ Sí | ❌ Sí | ❌ Sí | ❌ Sí |
| API semánticamente rica                 | ✅ Rica | ✅ Media | ✅ Media | ⚠️ | ❌ | ❌ |
| Arquitectura modular/facade             | ✅ Sí | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Type hinting completo y PEP 561         | ✅ Sí | ❌ Limitado | ❌ Limitado | ❌ No | ❌ No | ❌ No |
| **Alto Rendimiento (~1M ops/sec)**      | **✅ Sí** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Memoria Optimizada (`__slots__`)**    | **✅ Sí** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| Localización nativa (Sin Babel)         | ✅ Sí | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| API dedicada de Rangos/Periodos         | ✅ Sí | ✅ Sí | ⚠️ Básico | ⚠️ Básico | ❌ No | ❌ No |
| Aritmética de fechas (suma/resta)       | ✅    | ✅        | ✅    | ✅        | ❌        | ❌   |
| Parsing flexible (string, dict, dt)     | ✅    | ✅        | ✅    | ⚠️        | ✅        | ❌   |
| Testeada con coverage ≥ 97%             | ✅    | ❓        | ❓    | ❌        | ❌        | ❌   |
| Puede reemplazar `datetime` nativo      | ✅    | ✅        | ✅    | ❌        | ❌        | ❌   |
| Licencia permisiva (MIT / BSD)          | ✅    | ✅        | ✅    | ✅        | ✅        | ✅   |
| Mantenimiento activo                    | ✅    | ✅        | ✅    | ❌        | ✅        | ⚠️   |

> **Mirá los números:** Para métricas detalladas de rendimiento (Velocidad, Memoria, Perfilado), revisá nuestra **[Suite de Benchmarks](https://github.com/roldriel/eones/blob/master/benchmarks/README.md)**.

---

## 📚 Documentación y Ejemplos

Ejemplos completos y documentación disponibles:

### 📖 Ejemplos Principales
- **[Uso Básico](https://github.com/roldriel/eones/blob/master/examples/es/uso_basico.md)** - Importación de librería, creación de fechas, formateo, operaciones básicas
- **[Uso Avanzado](https://github.com/roldriel/eones/blob/master/examples/es/uso_avanzado.md)** - Truncamiento, redondeo, rangos de períodos, comparaciones
- **[Deltas Completos](https://github.com/roldriel/eones/blob/master/examples/es/deltas_completo.md)** - Arquitectura dual de deltas, intervalos de calendario vs duración
- **[Casos de Uso](https://github.com/roldriel/eones/blob/master/examples/es/casos_de_uso.md)** - Ejemplos del mundo real: cálculo de edad, ciclos de facturación, reportes
- **[Manejo de Errores](https://github.com/roldriel/eones/blob/master/examples/es/manejo_errores.md)** - Jerarquía de excepciones, creación segura de fechas, validación
- **[Formateo y Serialización](https://github.com/roldriel/eones/blob/master/examples/es/formateo_serializacion.md)** - ISO 8601, exportación/importación JSON, integración con APIs
- **[Configuración de Semana](https://github.com/roldriel/eones/blob/master/examples/es/configuracion_semana.md)** - Configuración del primer día de semana, estándares ISO vs US, detección de fin de semana

### 🔗 Ejemplos de Integración
- **Django**: Campos personalizados para modelos
- **SQLAlchemy**: Tipos de columna especializados  
- **APIs REST**: Utilidades de serialización

---

## 🔧 Tests y cobertura

```bash
tox
```

```bash
coverage html && open htmlcov/index.html
```

---

## 📖 Requisitos

- Python 3.9 o superior
- (Opcional) `tzdata` si usás zonas horarias en sistemas sin base local de zoneinfo

---

## 📝 Licencia

MIT © 2025 — Rodrigo Ezequiel Roldán  
[Ver licencia completa](https://github.com/roldriel/eones/blob/master/LICENSE.md)
