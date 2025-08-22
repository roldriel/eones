# Eones
![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-manual-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-97%25-blue?style=for-the-badge)
![Tox](https://img.shields.io/badge/Tested%20with-tox-yellowgreen?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/eones?style=for-the-badge)
![ChatGPT](https://img.shields.io/badge/ChatGPT-Collaborator-lightgrey?style=for-the-badge&logo=openai)

---

> Compatible con Python 3.9+ · Sin dependencias externas · Portátil y liviana

---

## ✨ ¿Qué es Eones?

Eones es una librería minimalista, sin dependencias externas, para trabajar con fechas y operaciones de tiempo de manera expresiva, clara y poderosa. Inspirada en la semántica natural del lenguaje, permite manipular, comparar y transformar fechas como si fueran entidades vivas.

> *“No está muerto lo que yace eternamente, y con el paso de extraños eones, incluso la muerte puede morir.”*  
> — *Abdul Alhazred*, Necronomicón

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
z.add(months=1, days=3)  # -> agregar 3 dias and 1 mes

print(z.format("%Y-%m-%d"))  # → 2025-07-18
print(z.diff_for_humans("2025-06-10"))  # → en 5 días
print(z.diff_for_humans("2025-06-20", locale="es"))  # → hace 5 días
```

---

## 🔍 Características principales

- ✅ Parsers automáticos para `str`, `dict`, `datetime`, `Eones`
- ✅ Agregado de días, meses, años, minutos y segundos
- ✅ Comparación de fechas (misma semana, dentro del año, entre rangos)
- ✅ Rango de día / semana / mes / trimestre / año completo
- ✅ Truncamiento y redondeo por unidad
- ✅ Soporte completo para `ZoneInfo` (PEP 615)
- ✅ Sin dependencias externas
- ✅ Conversión a `datetime`, `date`, y tipos nativos
- ✅ Diferencias expresivas con `diff_for_humans` y soporte de idiomas

Podés agregar más idiomas creando un archivo en `eones/locales/` con las
traducciones para tu idioma. Por ejemplo, `fr.py` para francés.

Manejo de errores

Eones muestra excepciones claras derivadas de `EonesError`. Las zonas horarias no válidas generan `InvalidTimezoneError`, mientras que las cadenas no analizables generan `InvalidFormatError`.

---

## 🧾 Comparación con otras librerías

| Característica                            | Eones | Pendulum | Arrow | Delorean | dateutil | pytz |
|-------------------------------------------|:-----:|:--------:|:-----:|:--------:|:--------:|:----:|
| API moderna y consistente                  | ✅    | ✅        | ✅    | ⚠️        | ❌        | ❌   |
| Manipulación de fechas (add/subtract)     | ✅    | ✅        | ✅    | ✅        | ❌        | ❌   |
| Parsing flexible (string, dict, datetime) | ✅    | ✅        | ✅    | ⚠️        | ✅        | ❌   |
| Soporte nativo de zonas horarias          | ✅    | ✅        | ✅    | ✅        | ⚠️        | ✅   |
| Sin dependencias externas                 | ✅    | ❌        | ❌    | ❌        | ❌        | ❌   |
| Testeada con coverage ≥ 97%               | ✅    | ❓        | ❓    | ❌        | ❌        | ❌   |
| Apta para reemplazar `datetime` directo   | ✅    | ✅        | ✅    | ❌        | ❌        | ❌   |
| Licencia permisiva (MIT / BSD)            | ✅    | ✅        | ✅    | ✅        | ✅        | ✅   |
| Mantenimiento activo                      | ✅    | ✅        | ✅    | ❌        | ✅        | ⚠️   |

---

## 📚 Ejemplos avanzados

Podés encontrar más ejemplos en:

- [examples/basic_usage.py](examples/basic_usage.py)
- [examples/advanced_usage.py](examples/advanced_usage.py)
- [examples/labor_calendar.py](examples/labor_calendar.py)

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
- (Opcional) `tzdata` si usás zonas horarias en sistemas sin base local

---

## 📝 Licencia

MIT © 2025 — Rodrigo Ezequiel Roldán  
[Ver licencia completa](LICENSE.md)
