# 🗺️ Roadmap de Eones

Este roadmap lista las funcionalidades planificadas para futuras versiones de `Eones`, priorizando simplicidad, completitud y ausencia de dependencias externas.

---

## 🎯 Visión General

Eones busca ser la librería de fechas en Python más clara, minimalista y segura, cubriendo las necesidades reales de desarrollo sin overhead innecesario, con compatibilidad multiplataforma (3.9+) y sin dependencias más allá de la standard library.

---

## 📋 Estado Actual

### ✅ Funcionalidades Completamente Implementadas

- **Clase Date completa**: Manejo robusto de fechas con zona horaria
- **Clase Delta**: Intervalos de tiempo con años, meses, días, horas, etc.
- **Parsing flexible**: Múltiples formatos de entrada soportados
- **Humanización localizada**: `diff_for_humans` en inglés y español
- **Rangos de períodos**: día, semana, mes, año, trimestre
- **Navegación por días de la semana**: `next_weekday`, `previous_weekday`
- **Operaciones temporales**: suma, resta, comparaciones
- **Truncamiento y redondeo**: `floor`, `ceil`, `round`
- **Serialización**: `to_dict`, `to_string`, `to_datetime`

### 🚀 Performance y Calidad (v1.4.x)
- **Benchmarks**: Suite completa de comparación y profiling
- **Optimización**: Lazy parser y fast paths (20% más rápido)
- **Calidad**: 98% coverage y typing estático completo

### ✅ v1.5.0 — Completada (Febrero 2026)
- **Serialización JSON**: `.for_json()` nativo en `Date` y `Delta`
- **Propiedades extendidas**: `quarter`, `iso_week`, `iso_year` en `Date`
- **Soporte fiscal**: `fiscal_year()`, `fiscal_quarter()` en `Date`
- **Fechas especiales**: `easter_date(year)` expuesta a través de `Eones`
- **Iterador de rangos**: `range_iter(start, end, step)` eficiente en memoria
- **Parsing ambiguo**: Opciones `day_first` y `year_first` en `Eones` y `Parser`
- **Rendimiento**: >1.3M ops/sec en ISO parsing (~6.7x más rápido que Pendulum)
- **Operadores mejorados**: `__add__`/`__sub__` con `Delta` además de `timedelta`
- **Parsing ISO 8601 con offset**: Soporte completo para `+03:00`, `-05:00`
- **API ergonómica**: `add()` y `subtract()` con mejor interfaz declarativa
- **PEP 561**: Marcador `py.typed` para soporte de verificadores de tipos
- **Tests de integración**: Cobertura comprehensiva para Django, SQLAlchemy y serializers
- **Documentación**: Guías de integración y documentación Sphinx con tema Furo

---

## 🚀 Funcionalidades Pendientes

---
- **Current Version:** v1.6.0
- **Next Milestone:** v1.7.0 (Extensiones ISO, Precisión y Confiabilidad)

### ✅ v1.6.0 — Completada (Febrero 2026)
- **Calendarios de feriados**: 7 calendarios nacionales (`America/Argentina`, `America/US`, `Europe/France`, `Europe/Germany`, `Europe/Spain`, `Asia/Japan`, `Oceania/Australia`)
- **Días hábiles**: `is_business_day()`, `next/previous_business_day()`, `add/subtract_business_days(n)`
- **Métricas**: `count_business_days()`, `count_weekends()`, `count_holidays()`, `time_until_weekend()`, `time_until_business_day()`
- **Registro custom**: `register_calendar()`, `available_calendars()`
- **Formateo localizado**: `format_locale("DD de MMMM de YYYY", locale="es")` con tokens
- **Locale japonés**: `diff_for_humans(locale="ja")` con sufijos
- **Nombres localizados**: `MONTHS` y `DAYS` en 5 idiomas (en, es, fr, de, ja)
- **Constructor con defaults**: `Eones(value, locale="es", calendar="America/Argentina")`

## 🆕 **PRÓXIMAS FUNCIONALIDADES**

---

### 🔖 **v1.7.0 – Extensiones ISO, Precisión y Confiabilidad**

**Prioridad:** Media | **Estado:** Planeado

> **Completa soporte ISO 8601 y mejora la integridad técnica del núcleo**

- [ ] **Métodos para ISO 8601 semana/año** *(Extiende propiedades ISO actuales)*
  - `from_iso_week()`, `.iso_week`
- [ ] **Monotonic Drift Protection** *(Nueva funcionalidad de confiabilidad)*
  - Implementar protección contra saltos de reloj del sistema (NTP sync) usando `time.monotonic()`
  - Garantizar que las duraciones calculadas entre instancias en memoria sean inmunes a cambios de hora del SO
- [ ] **Año fiscal y calendario contable** *(Extiende rangos de períodos)*
  - `fiscal_quarter(date, fiscal_start_month=4)`
  - `fiscal_year(date, fiscal_start_month=4)`
  - Métodos para períodos fiscales personalizados
- [ ] **Soporte para precisión subsegundo** *(Mejora precisión actual)*
  - Microsegundos y nanosegundos para sistemas de alta resolución

---

### 🔖 **v1.8.0 – Razonamiento Avanzado: Intervalos y Calendarios Básicos**

**Prioridad:** Media | **Estado:** Planeado

> **Introduce álgebra de tiempo y primeros calendarios alternativos**

- [ ] **Continuous Timespans / Intervals** *(Nueva funcionalidad mayor)*
  - Abstracción de lapsos de tiempo dinámicos (no atados a períodos fijos)
  - **Álgebra de Intervalos:** Métodos `.overlaps(other)`, `.intersect(other)`, `.union(other)`
  - **Relaciones de Allen:** Implementación de las 13 relaciones formales
- [ ] **Soporte parcial para calendario Juliano** *(Funcionalidad especializada)*
  - `from_julian()`, `to_julian()`
  - Conversión básica entre gregoriano y juliano
- [ ] **ISO 8601 completo**
  - Soporte completo para semanas ISO: `.iso_week_date()`, `.from_iso_week_date()`

---

### 🔖 **v1.9.0 – Productividad (DX) y Calendarios Avanzados**

**Prioridad:** Media | **Estado:** Planeado

> **Herramientas de desarrollo y expansión calendárica**

- [ ] **Temporal Anchoring / Native Mocking** *(Nueva funcionalidad de testing)*
  - Sistema de "congelación" de tiempo nativo (`Eones.freeze()`, `Eones.travel()`)
  - Context managers para tests deterministas sin dependencias externas
- [ ] **Semantic Temporal Adjusters** *(Nueva funcionalidad de ergonomía)*
  - Implementar ajustadores declarativos: `.adjust(LastDayOfMonth())`, `.adjust(NextBusinessDay())`
  - Soporte para reglas complejas: `.adjust(NthWeekdayInMonth(2, "Monday"))`
- [ ] **Soporte extendido para calendario Juliano**
  - Conversión completa y métodos `.to_julian_day()`, `.from_julian_day()`
- [ ] **Soporte básico para calendarios no gregorianos**
  - Calendario hebreo e islámico (funcionalidades básicas de conversión)

---

### 🔖 **v1.10.0 – Recurrencias y Procesamiento de Lenguaje**

**Prioridad:** Media | **Estado:** Planeado

> **Funcionalidades para sistemas de eventos y agendamiento**

- [ ] **Fuzzy Parsing (Parseo Difuso)** *(Nueva funcionalidad avanzada)*
  - Soporte para lenguaje natural: "next friday", "3 days ago", "tomorrow at 5pm"
- [ ] **API para reglas recurrentes y expresiones cron**
  - `every("month", on_day=15)`, `from_cron("0 9 * * 1-5")`
  - Recurrencias condicionales (ej: "segundo lunes no feriado del mes")
- [ ] **Soporte nativo de RRULE completo (RFC 2445)**
  - Implementación nativa de reglas de recurrencia iCalendar
- [ ] **Filtros condicionales avanzados**
  - "excluir feriados" o "solo días hábiles" en recurrencias

---

### 🔖 **v1.11.0 – Precisión Científica y Especialización Empresarial**

**Prioridad:** Baja | **Estado:** Investigación

> **Funcionalidades para casos de uso extremos y alta especialización**

- [ ] **Precisión Astronómica/Científica** *(Nueva funcionalidad especializada)*
  - Soporte para **Julian Day Numbers (JDN)** y Leap Seconds
  - Soporte para escalas de tiempo alternativas (TDB)
- [ ] **Calendarios empresariales especializados**
  - Calendario bancario, escolar y corporativo personalizable
- [ ] **Ajuste automático a días hábiles**
  - `adjust_to_business_day(date, direction='forward/backward/nearest')`
- [ ] **Soporte para múltiples calendarios simultáneos**
  - Intersección de calendarios (ej: bancario + feriados nacionales)

---

## 🤝 Contribución

Si deseas contribuir a alguna funcionalidad:

1. Revisa los issues etiquetados como `help wanted`
2. Abre un PR referenciando la versión planeada
3. Asegúrate de seguir la filosofía **minimalista y sin dependencias** de Eones

---

## 📝 Notas

> ⚠️ Este roadmap es incremental y flexible. Se priorizan funcionalidades de **alto impacto, bajo costo** y alineadas con la filosofía minimalista de Eones.

> 📊 **ESTRUCTURA DE PRIORIDADES:**
> - 🆕 **NUEVAS:** Funcionalidades completamente nuevas
> - 📈 **ORDEN:** Primero completar, luego innovar

> 📅 **Última actualización:** Febrero 2026
> 🔖 **Versión actual:** 1.6.0

---

*Para más información sobre el uso actual de Eones, consulta [DOCUMENTACION.md](./DOCUMENTACION.md)*
