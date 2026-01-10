# 📦 CHANGELOG

Todas las versiones están documentadas en este archivo.

## [1.4.1] - 09-01-2026

### Corregido
- Se estandarizaron todos los nombres de archivo de documentación a mayúsculas (`README.md`, `LICENSE.md`, `CHANGELOG.md`) para asegurar compatibilidad con CI en Linux
- Se eliminó el input inválido `install-project` del workflow de documentación para resolver advertencia
- Se aseguró la correcta ejecución del pipeline de release incrementando la versión para evitar conflictos en PyPI

## [1.4.0] - 09-01-2026

### Agregado
- Suite completo de benchmarks con 4 scripts:
  - `comparison.py`: Comparación de rendimiento contra competidores (Pendulum, Arrow, dateutil, Delorean)
  - `microbenchmarks.py`: Testing de rendimiento de métodos aislados
  - `memory.py`: Análisis de huella de memoria con pympler
  - `profiling.py`: Perfilado de CPU con cProfile
- Documentación de benchmarks integrada en Sphinx (`docs/source/benchmarks/`)
- Tablas de comparación mejoradas en README con filas de Performance y Memory
- Roadmap del proyecto (`ROADMAP.md`) documentando planes de desarrollo futuros

### Rendimiento
- Inicialización lazy del parser: 20% más rápido en instanciación de fechas
- Optimizaciones de fast path para parsing ISO con concatenación de strings
- Bypass del constructor para fechas conocidas como válidas en `from_iso`

### Mejorado
- Cobertura de tests incrementada de 94% a 98% (+439 tests pasando ahora)
- Todos los warnings de Pylint resueltos (puntaje 10/10 alcanzado)
- Todos los errores de tipo de Mypy corregidos (type checking limpio)
- Configuración del proyecto consolidada en `pyproject.toml`
- Tests de integración reorganizados para mejor mantenibilidad

### Cambiado
- Eliminados `.coveragerc`, `.pylintrc`, `pytest.ini` (migrados a `pyproject.toml`)
- Actualizado `tox.ini` para corregir configuración de `allowlist_externals` y `pip-audit`
- Docstrings compactados en `date.py` para reducir cantidad de líneas del módulo

---

## [1.3.6] - 19-01-2025

### Corregido
- Se resolvieron las advertencias de acceso a contexto en los workflows de GitHub Actions ([13069b4](https://github.com/roldriel/eones/commit/13069b4))
- Se corrigió el error de sintaxis de comillas anidadas en el mensaje de commit del workflow de release
- Se agregaron verificaciones condicionales para outputs de jobs para prevenir acceso a contexto inválido

### Cambiado
- Se actualizó la versión a 1.3.6 en todos los archivos del proyecto
- Se mejoró la robustez de los workflows con valores de respaldo para outputs de tag y versión

---

## [1.3.5] - 17-01-2025

### Corregido
- Se actualizaron los enlaces de ejemplos a URLs completas de GitHub para compatibilidad con PyPI
- Se corrigieron enlaces relativos rotos en archivos README cuando se muestran en PyPI

### Cambiado
- Se actualizó la versión a 1.3.5 en todos los archivos del proyecto
- Se mejoró la accesibilidad de la documentación en PyPI

---

## [1.3.3] - 26-08-2025

### Corregido
- Se corrigieron errores de formato de imports detectados por isort ([19752e6](https://github.com/roldriel/eones/commit/19752e6))

### Cambiado
- Se actualizó la versión a 1.3.3
- Se mejoró la calidad y consistencia del formato del código

---

## [1.3.2] - 25-08-2025

### Cambiado
- Actualización de versión para desarrollo ([652c2ac](https://github.com/roldriel/eones/commit/652c2ac))

---

## [1.3.1] - 25-08-2025

### Corregido
- Se agregó el método estático is_valid_format faltante a la clase Eones
- Se corrigió la advertencia de pylint import-outside-toplevel
- Se corrigió error de sintaxis en docstring

### Cambiado
- Se actualizó git-cliff-action de v2 a v3 para mayor estabilidad
- Se agregó variable de entorno OUTPUT al flujo de trabajo de release
- Actualización de versión a 1.3.1 ([288752f](https://github.com/roldriel/eones/commit/288752f))

---

## [1.2.0] - 25-06-2025
- Se añadió `diff_for_humans` con reconocimiento de configuración regional mediante el nuevo módulo `humanize`.
- Se introdujo el paquete `eones/locales/` para mensajes de idioma.
- Se expuso `diff_for_humans` en las clases `Date` y `Eones`.
- Se documentó la extensibilidad del lenguaje y se añadieron pruebas.
- Se añadieron métodos de comparación `Date.is_same_day`, `Date.is_before`, `Date.is_after` y `Date.days_until`
- Nueva propiedad `Date.as_local` y se renombró el método de conversión de zona horaria a `as_zone`
- Las pruebas de integración se omiten si faltan dependencias opcionales como Django o SQLAlchemy

---

## [1.1.0] - 13-06-2025
- Se actualizó `pyproject.toml` a `1.1.0`.
- Se actualizó `README.md` a `1.1.0`.
- Se añadieron cadenas de documentación a todos los métodos y clases en el código fuente y las pruebas.
- Se añadieron pruebas para todos los métodos y clases.
- Se alcanzó una cobertura del `99%` para las pruebas.
- Se añadieron métodos para gestionar rangos y puntos. - Se corrigieron errores en los métodos de comparación.
- Se añadieron errores para su posterior corrección.

---

## [1.0.0] - 2025-05-19

### Added
- Primera versión estable de la librería `eones`.
- Parser unificado para `str`, `dict`, `datetime`.
- Soporte de zonas horarias con `ZoneInfo`.
- Métodos de truncamiento, agregación, comparación y rangos.
- Integraciones opcionales con `Django`, `SQLAlchemy`, `Serializers`.

### Changed
- Interfaz centralizada en la clase `Eones`.

---

## Histórico

Este proyecto está diseñado para ser minimalista, multiplataforma y 100% basado en la biblioteca estándar de Python.
