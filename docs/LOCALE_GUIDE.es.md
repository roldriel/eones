# Guía de Extensión de Locales

Eones soporta múltiples idiomas para el formateo de fechas legible por humanos y descripciones de tiempo relativo (ej., "hace 2 días"). Esta guía explica cómo agregar un nuevo idioma a la librería.

## 📁 Estructura

Todos los idiomas se encuentran en `src/eones/locales/`. Cada archivo debe nombrarse con el código de idioma ISO 639-1 de dos letras (ej., `en.py`, `es.py`, `fr.py`).

## 🧱 Componentes Requeridos

Un archivo de idioma debe definir las siguientes constantes:

1. **MONTHS**: Nombres completos de los meses (1-12).
2. **MONTH_ABBRS**: Nombres abreviados de los meses (1-12).
3. **DAYS**: Nombres completos de los días (0=Lunes a 6=Domingo).
4. **DAY_ABBRS**: Nombres abreviados de los días (0-6).
5. **RELATIVE_PATTERNS**: Diccionario con plantillas para tiempo relativo (pasado/futuro).

### Ejemplo: `fr.py` (Francés)

```python
MONTHS = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

MONTH_ABBRS = {
    1: "Janv.", 2: "Févr.", 3: "Mars", 4: "Avril",
    5: "Mai", 6: "Juin", 7: "Juil.", 8: "Août",
    9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Déc."
}

DAYS = {
    0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi",
    4: "Vendredi", 5: "Samedi", 6: "Dimanche"
}

DAY_ABBRS = {
    0: "Lun.", 1: "Mar.", 2: "Mer.", 3: "Jeu.",
    4: "Ven.", 5: "Sam.", 6: "Dim."
}

RELATIVE_PATTERNS = {
    "now": "maintenant",
    "past": "il y a {0} {1}",
    "future": "dans {0} {1}",
    "units": {
        "second": ["seconde", "secondes"],
        "minute": ["minute", "minutes"],
        "hour": ["heure", "heures"],
        "day": ["jour", "jours"],
        "week": ["semaine", "semaines"],
        "month": ["mois", "mois"],
        "year": ["an", "ans"]
    }
}
```

## 🧪 Probando tu Idioma

Después de agregar el archivo, podés verificarlo usando el método `diff_for_humans`:

```python
from eones import Eones

e = Eones("2024-01-01")
print(e.diff_for_humans("2024-01-05", locale="fr")) # -> il y a 4 jours
```

Para integrar permanentemente el idioma, agregá un caso de prueba en `tests/unit/test_humanize.py`.
