# Locale Extension Guide

Eones supports multiple languages for human-readable date formatting and relative time descriptions (e.g., "shared in 2 days"). This guide explains how to add a new locale to the library.

## 📁 Structure

All locales are located in `src/eones/locales/`. Each file must be named with a two-letter ISO 639-1 language code (e.g., `en.py`, `es.py`, `fr.py`).

## 🧱 Required Components

A locale file must define the following constants:

1. **MONTHS**: Full month names (1-12).
2. **MONTH_ABBRS**: Abbreviated month names (1-12).
3. **DAYS**: Full day names (0=Monday to 6=Sunday).
4. **DAY_ABBRS**: Abbreviated day names (0-6).
5. **RELATIVE_PATTERNS**: Dictionary with templates for relative time (past/future).

### Example: `fr.py` (French)

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

## 🧪 Testing your Locale

After adding the file, you can verify it using the `diff_for_humans` method:

```python
from eones import Eones

e = Eones("2024-01-01")
print(e.diff_for_humans("2024-01-05", locale="fr")) # -> il y a 4 jours
```

To permanently integrate the locale, add a test case in `tests/unit/test_humanize.py`.
