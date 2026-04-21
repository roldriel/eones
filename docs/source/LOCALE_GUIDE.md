# Locale Extension Guide

Eones supports multiple languages for human-readable relative time descriptions (e.g., "2 days ago", "hace 2 días"). This guide explains how to add a new locale to the library.

## Supported Locales

| Code | Language | Example (past)       | Example (future)     |
|------|----------|----------------------|----------------------|
| `en` | English  | 2 days ago           | in 2 days            |
| `es` | Spanish  | hace 2 días          | en 2 días            |
| `fr` | French   | il y a 2 jours       | dans 2 jours         |
| `de` | German   | vor 2 Tagen          | in 2 Tagen           |
| `ja` | Japanese | 2 日前               | 2 日後               |

## Structure

All locales are located in `src/eones/locales/`. Each file must be named with a two-letter ISO 639-1 language code (e.g., `en.py`, `es.py`, `fr.py`, `de.py`, `ja.py`).

Locales are discovered automatically via dynamic import. No registration step is needed.

## Required Components

A locale file must define a `MESSAGES` dictionary with the following keys:

| Key        | Type               | Description                              |
|------------|--------------------|------------------------------------------|
| `past`     | `str`              | Prefix/suffix for past times             |
| `future`   | `str`              | Prefix/suffix for future times           |
| `just_now` | `str`              | Label when difference < 1 second         |
| `year`     | `(str, str)`       | Singular and plural forms                |
| `month`    | `(str, str)`       | Singular and plural forms                |
| `week`     | `(str, str)`       | Singular and plural forms                |
| `day`      | `(str, str)`       | Singular and plural forms                |
| `hour`     | `(str, str)`       | Singular and plural forms                |
| `minute`   | `(str, str)`       | Singular and plural forms                |
| `second`   | `(str, str)`       | Singular and plural forms                |
| `position` | `str` *(optional)* | `"suffix"` to place marker after label   |

### Example: Adding Italian (`it.py`)

```python
"""src/eones/locales/it.py"""

MESSAGES = {
    "past": "fa",
    "future": "tra",
    "year": ("anno", "anni"),
    "month": ("mese", "mesi"),
    "week": ("settimana", "settimane"),
    "day": ("giorno", "giorni"),
    "hour": ("ora", "ore"),
    "minute": ("minuto", "minuti"),
    "second": ("secondo", "secondi"),
    "just_now": "proprio adesso",
}
```

## Formatting Rules

The output format depends on the locale:

- **English** (`en`): `"{count} {label} {past}"` / `"{future} {count} {label}"` (e.g., "2 days ago" / "in 2 days")
- **Suffix locales** (`position: "suffix"`): `"{count} {label}{marker}"` (e.g., "2 日前" / "2 日後") — no space before marker
- **All other locales**: `"{past/future} {count} {label}"` (e.g., "hace 2 días" / "il y a 2 jours")

The optional `position` key controls marker placement. When set to `"suffix"`, the past/future marker is appended directly after the label without a space. This is used for languages like Japanese where the temporal marker follows the unit.

## Testing your Locale

After adding the file, verify it using `diff_for_humans`:

```python
from eones import Eones

e = Eones("2024-01-01")
print(e.diff_for_humans("2024-01-05", locale="it"))  # -> fa 4 giorni
```

To permanently integrate the locale, add a test case in `tests/unit/test_humanize.py`.

## Fallback Behavior

If a locale code is not found, Eones falls back to English (`en`) automatically.
