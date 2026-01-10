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
- **Truncamiento y redondeo**: `floor`, `ceil`, `round`
- **Serialización**: `to_dict`, `to_string`, `to_datetime`

### 🚀 Performance y Calidad (v1.4.0)
- **Benchmarks**: Suite completa de comparación y profiling
- **Optimización**: Lazy parser y fast paths (20% más rápido)
- **Calidad**: 98% coverage y typing estático completo

---

## 🚀 Funcionalidades Pendientes

---

## 🔥 **CRÍTICO - Completar Funcionalidades Existentes**

### 🔖 **v1.5.0 – Extensiones Críticas de Funcionalidades Actuales**

**Prioridad:** CRÍTICA | **Estado:** Inmediato

> **Objetivo:** Completar y perfeccionar las funcionalidades ya implementadas antes de agregar nuevas características.

- [x] **Métodos semánticos de calendario** *(Extiende clase Date actual)*
  - `Date.is_leap_year()` - Verificar si el año es bisiesto
  - `Date.is_weekend()` - Verificar si es fin de semana
  - `Date.is_monday()`, `is_tuesday()`, etc. - Verificar día específico de la semana
- [x] **Mejoras en operadores de Date** *(Completa operaciones temporales)*
  - Soporte para `__add__` y `__sub__` con objetos `Delta` además de `timedelta`
  - Operadores más intuitivos para suma/resta de períodos
- [x] **Parsing ISO 8601 con offset completo** *(Extiende parsing flexible actual)*
  - Soporte para `+03:00`, `-05:00` en parsing de strings
  - Extender parsing con `%z` para offsets horarios
- [ ] **Método `.for_json()`** *(Completa serialización actual)*
  - Serialización JSON directa en objetos Date/Eones
- [ ] **Mejoras en interfaz Eones** *(Perfecciona interfaz actual)*
  - Métodos declarativos mejorados: `add(...)` y `subtract(...)` con mejor ergonomía
  - Validaciones y mensajes de error más descriptivos
- [ ] **Propiedades fiscales y ISO extendidas** *(Extiende rangos de períodos)*
  - `Date.quarter`, `fiscal_year(start_month)`, `fiscal_quarter(start_month)`
  - Exposición directa de propiedades ISO (número de semana, año ISO)
- [ ] **Iterador de rangos** *(Completa rangos de períodos actuales)*
  - Implementar `range_iter(start, end, step)` para iteración declarativa

---

## 🆕 **NUEVAS FUNCIONALIDADES**

### 🔖 **v1.5.0 – Funcionalidades Especiales y Parsing Avanzado**

**Prioridad:** Alta | **Estado:** Planeado

- [ ] **Fecha de Pascua y fechas especiales** *(Nueva funcionalidad)*
  - `easter_date(year)` - Calcular fecha de Pascua para un año dado
  - Soporte para otras fechas especiales calculadas
- [ ] **Normalización de entrada ambigua** *(Nueva funcionalidad)*
  - Manejo inteligente de formatos de fecha ambiguos (DD/MM vs MM/DD)
  - Configuración de preferencias regionales para parsing ambiguo

---

### 🔖 **v1.6.0 – Calendario Laboral y Métricas**

**Prioridad:** Alta | **Estado:** Planeado

> **Funcionalidades de alto valor para aplicaciones empresariales**

- [ ] **Soporte de feriados y días hábiles** *(Nueva funcionalidad crítica)*
  - `is_holiday(date, calendar='AR')` con soporte para calendario custom
  - `is_business_day(date, weekend={5,6}, calendar='AR')`
  - `next_business_day(date, direction='forward')`
  - `add_business_days(n)`, `subtract_business_days(n)`
  - `count_business_days(start, end)`, `count_weekends(start, end)`

---

### 🔖 **v1.7.0 – Internacionalización Avanzada**

**Prioridad:** Media | **Estado:** Planeado

> **Extiende humanización localizada actual**

- [ ] **Formateo localizado completo** *(Extiende capacidades actuales)*
  - `format_locale("DD de MMMM de YYYY", locale="es")`
  - Diccionarios internos de nombres de meses/días para idiomas comunes
- [ ] **Soporte multilenguaje extendido** *(Extiende diff_for_humans actual)*
  - Más idiomas para `diff_for_humans(locale=...)`
  - Localización de nombres de meses y días de la semana

---

### 🔖 **v1.8.0 – Extensiones ISO y Precisión**

**Prioridad:** Media | **Estado:** Planeado

> **Completa soporte ISO 8601 y mejora precisión temporal**

- [ ] **Métodos para ISO 8601 semana/año** *(Extiende propiedades ISO actuales)*
  - `from_iso_week()`, `.iso_week`
- [ ] **Año fiscal y calendario contable** *(Extiende rangos de períodos)*
  - `fiscal_quarter(date, fiscal_start_month=4)`
  - `fiscal_year(date, fiscal_start_month=4)`
  - Métodos para períodos fiscales personalizados
- [ ] **Métricas temporales integradas** *(Extiende funcionalidades de cálculo)*
  - `count_weekends(start, end)` - Contar fines de semana en un rango
  - `count_holidays(start, end, calendar='AR')` - Contar feriados
  - `time_until_weekend()`, `time_until_business_day()`
- [ ] **Soporte para precisión subsegundo** *(Mejora precisión actual)*
  - Microsegundos y nanosegundos para sistemas de alta resolución
  - Métodos `.microsecond`, `.nanosecond` si se justifica por casos de uso

---

### 🔖 **v1.9.0 – Calendarios Alternativos Básicos**

**Prioridad:** Baja | **Estado:** Planeado

> **Funcionalidades especializadas de menor prioridad**

- [ ] **Soporte parcial para calendario Juliano** *(Nueva funcionalidad especializada)*
  - `from_julian()`, `to_julian()`
  - Conversión básica entre gregoriano y juliano

---

- [ ] **ISO 8601 completo** *(Extiende soporte ISO actual)*
  - Soporte completo para semanas ISO
  - `.iso_week_date()`, `.from_iso_week_date()`

---

- [ ] **Soporte extendido para calendario Juliano** *(Extiende v1.9.0)*

### 🔖 **v1.10.0 – Calendarios Alternativos Avanzados**

**Prioridad:** Muy Baja | **Estado:** Investigación

> **Funcionalidades muy especializadas - solo si hay demanda**

- [ ] **Soporte extendido para calendario Juliano** *(Extiende v1.9.0)*
  - Conversión completa entre gregoriano y juliano
  - Métodos `.to_julian_day()`, `.from_julian_day()`
- [ ] **Soporte básico para calendarios no gregorianos** *(Nueva funcionalidad muy especializada)*
  - Calendario hebreo (básico)
  - Calendario islámico (básico)
  - Solo si hay demanda real de usuarios

---

### 🔖 **v1.11.0 – Recurrencias y Reglas Avanzadas**

**Prioridad:** Media | **Estado:** Muy Largo Plazo

> **Funcionalidades completamente nuevas de alta complejidad**

- [ ] **API para reglas recurrentes simples** *(Nueva funcionalidad mayor)*
  - `every("month", on_day=15)`
  - `every("week", on_weekday="monday")`
  - `every("year", on_month=6, on_day=15)`
- [ ] **Soporte básico para expresiones cron** *(Nueva funcionalidad)*
  - Parsing y evaluación de expresiones cron simples
  - `from_cron("0 9 * * 1-5")` para días laborables a las 9 AM
- [ ] **Recurrencias condicionales** *(Funcionalidad avanzada)*
  - "segundo lunes no feriado del mes"
  - "último día hábil del mes"
  - Lógica condicional avanzada
- [ ] **Soporte para filtros condicionales** *(Extiende calendario laboral)*
  - Ej: "excluir feriados" o "solo días hábiles"
- [ ] **Soporte nativo de RRULE completo (RFC 2445)** *(Funcionalidad muy avanzada)*
  - Implementación nativa de reglas de recurrencia RFC 2445
  - Parsing y generación de RRULE strings
  - Compatibilidad con especificación completa de iCalendar
- [ ] **Integración opcional con `dateutil.rrule`** *(Solo si es necesario)*
  - Para RRULE completas manteniendo filosofía sin dependencias

---

### 🔖 **v1.12.0 – Calendarios Especializados Avanzados**

**Prioridad:** Muy Baja | **Estado:** Futuro Lejano

> **Extiende funcionalidades de calendario laboral para casos muy específicos**

- [ ] **Calendarios especializados** *(Extiende calendario laboral v1.6.0)*
  - Calendario bancario (días hábiles bancarios)
  - Calendario escolar (períodos lectivos)
  - Calendario corporativo personalizable
- [ ] **Ajuste automático a días hábiles** *(Extiende días hábiles v1.6.0)*
  - `adjust_to_business_day(date, direction='forward')`
  - `adjust_to_business_day(date, direction='backward')`
  - `adjust_to_business_day(date, direction='nearest')`
- [ ] **Soporte para múltiples calendarios simultáneos** *(Funcionalidad muy avanzada)*
  - Intersección de calendarios (ej: bancario + feriados nacionales)
  - `is_business_day(date, calendars=['banking', 'national'])`

---

## 🤝 Contribución

Si deseas contribuir a alguna funcionalidad:

1. Revisa los issues etiquetados como `help wanted`
2. Abre un PR referenciando la versión planeada
3. Asegúrate de seguir la filosofía **minimalista y sin dependencias** de Eones

---

## 📝 Notas

> 🔥 **FILOSOFÍA DE PRIORIZACIÓN:** Este roadmap prioriza **COMPLETAR** las funcionalidades existentes antes que agregar nuevas. Las funcionalidades críticas (v1.4.0) extienden y perfeccionan lo ya implementado.

> ⚠️ Este roadmap es incremental y flexible. Se priorizan funcionalidades de **alto impacto, bajo costo** y alineadas con la filosofía minimalista de Eones.

> 📊 **ESTRUCTURA DE PRIORIDADES:**
> - 🔥 **CRÍTICO:** Extensiones de funcionalidades existentes
> - 🆕 **NUEVAS:** Funcionalidades completamente nuevas
> - 📈 **ORDEN:** Primero completar, luego innovar

> 📅 **Última actualización:** Enero 2025  
> 🔖 **Versión actual:** 1.4.0

---

*Para más información sobre el uso actual de Eones, consulta [DOCUMENTACION.md](./DOCUMENTACION.md)*