# Locale-Aware Date Formatting

Eones provides `format_locale()` for formatting dates with localized month and day names. It supports 5 languages out of the box: English, Spanish, French, German, and Japanese.

## Format Tokens

| Token  | Description                     | Example (en)  | Example (es)   |
|--------|---------------------------------|---------------|----------------|
| `MMMM` | Full month name                | January       | enero          |
| `MMM`  | Abbreviated month name          | Jan           | ene            |
| `MM`   | Zero-padded month number        | 01            | 01             |
| `M`    | Month number without padding    | 1             | 1              |
| `dddd` | Full day name                   | Monday        | lunes          |
| `ddd`  | Abbreviated day name            | Mon           | lun            |
| `DD`   | Zero-padded day of month        | 05            | 05             |
| `D`    | Day without padding             | 5             | 5              |
| `YYYY` | Four-digit year                 | 2026          | 2026           |
| `YY`   | Two-digit year                  | 26            | 26             |
| `HH`   | Zero-padded hour (24h)          | 09            | 09             |
| `mm`   | Zero-padded minute              | 05            | 05             |
| `ss`   | Zero-padded second              | 00            | 00             |

## Basic Usage

```python
from eones import Eones

e = Eones("2026-05-25")

# English (default)
e.format_locale("MMMM DD, YYYY")           # "May 25, 2026"
e.format_locale("dddd, MMMM DD")           # "Monday, May 25"
e.format_locale("ddd DD MMM YYYY")         # "Mon 25 May 2026"
e.format_locale("MM/DD/YYYY")              # "05/25/2026"
```

## Setting a Default Locale

```python
# Locale is inherited by all subsequent calls
e = Eones("2026-05-25", locale="es")

e.format_locale("DD de MMMM de YYYY")      # "25 de mayo de 2026"
e.format_locale("dddd DD de MMMM")         # "lunes 25 de mayo"
e.format_locale("ddd DD MMM YYYY")         # "lun 25 may 2026"
```

## Per-Call Override

```python
e = Eones("2026-05-25", locale="es")

# Override the default locale for a single call
e.format_locale("dddd, MMMM DD", locale="en")   # "Monday, May 25"
e.format_locale("dddd, MMMM DD", locale="fr")   # "lundi, mai 25"
```

## All Supported Locales

### English (`en`)

```python
Eones("2026-03-15").format_locale("dddd, MMMM DD, YYYY")
# "Sunday, March 15, 2026"
```

### Spanish (`es`)

```python
Eones("2026-03-15", locale="es").format_locale("dddd DD de MMMM de YYYY")
# "domingo 15 de marzo de 2026"
```

### French (`fr`)

```python
Eones("2026-03-15", locale="fr").format_locale("dddd DD MMMM YYYY")
# "dimanche 15 mars 2026"
```

### German (`de`)

```python
Eones("2026-03-15", locale="de").format_locale("dddd, DD. MMMM YYYY")
# "Sonntag, 15. Marz 2026"
```

### Japanese (`ja`)

```python
Eones("2026-03-15", locale="ja").format_locale("YYYY年MM月DD日 (ddd)")
# "2026年03月15日 (日)"
```

## Combining with Time Components

```python
e = Eones("2026-05-25 14:30:45", locale="es")

e.format_locale("DD de MMMM de YYYY, HH:mm:ss")
# "25 de mayo de 2026, 14:30:45"

e.format_locale("ddd DD MMM - HH:mm")
# "lun 25 may - 14:30"
```

## Combining with diff_for_humans

The `locale` parameter works consistently across `format_locale` and `diff_for_humans`:

```python
e = Eones("2026-05-25", locale="fr")

e.format_locale("dddd DD MMMM YYYY")       # "lundi 25 mai 2026"
e.diff_for_humans("2026-05-20")             # "il y a 5 jours"
```

### Japanese Suffix Pattern

Japanese uses a suffix-style pattern for `diff_for_humans`:

```python
e = Eones("2026-05-25", locale="ja")

e.format_locale("YYYY年MM月DD日")           # "2026年05月25日"
e.diff_for_humans("2026-05-20")             # "5 日前"
e.diff_for_humans("2026-05-30")             # "5 日後"
```

## Adding New Locales

See the [Locale Extension Guide](../LOCALE_GUIDE) for instructions on adding new languages.
