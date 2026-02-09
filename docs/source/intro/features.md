# 🔍 Key Features

- ✅ **Zero external dependencies**: Pure Python (Python 3.9+)
- ✅ **Intuitive interface**: Simple, semantically rich and easy-to-use API
- ✅ **Modern timezone support**: Robust handling with `zoneinfo` (not `pytz`)
- ✅ **Flexible parsing**: Accepts multiple date formats automatically, including ISO 8601 with timezone offsets
- ✅ **Advanced temporal operations**: Deltas, ranges and semantic comparisons
- ✅ **Modular architecture**: Clear separation between `Date`, `Delta`, `Range` and utilities
- ✅ **Localization**: Support for multiple languages
- ✅ **Humanization**: Converts time differences to readable text
- ✅ **Complete type hinting**: Fully typed following PEP 561
- ✅ **Interoperability**: Compatible with Python's standard `datetime`

## Localization & Error Handling

You can add more languages by creating a new file in `eones/locales/` with the
translations for your locale. For example, `fr.py` for French.

Eones surfaces clear exceptions derived from `EonesError`. Invalid timezones
raise `InvalidTimezoneError`, while unparsable strings raise
`InvalidFormatError`.
