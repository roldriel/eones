# 📦 CHANGELOG

All versions are documented in this file.

## [1.2.0] - 2025-06-25
- Added locale-aware `diff_for_humans` via the new `humanize` module.
- Introduced `eones/locales/` package for language messages.
- Exposed `diff_for_humans` on `Date` and `Eones` classes.
- Documented language extensibility and added tests.
- Added comparison helpers `Date.is_same_day`, `Date.is_before`, `Date.is_after` and `Date.days_until`
- Added `Date.as_local` property and renamed timezone conversion method to `as_zone`
- Integration tests now skip if Django or SQLAlchemy are not installed

---

## [1.1.0] - 2025-06-13
- Updated `pyproject.toml` to `1.1.0`.
- Updated `README.md` to `1.1.0`.
- Added Docstrings to all methods and classes in the source code and tests.
- Added tests for all methods and classes.
- Reached `99%` coverage for tests.
- Added methods for handling ranges and periods.
- Fixed bugs in comparison methods.
- Added bugs for later fixes.

---

## [1.0.0] - 2025-05-19

### Added
- First stable release of the `eones` library.
- Unified parser for `str`, `dict`, and `datetime`.
- Timezone support using `ZoneInfo`.
- Truncation, aggregation, comparison, and range methods.
- Optional integrations for `Django`, `SQLAlchemy`, and `Serializers`.

### Changed
- Centralized interface using the `Eones` class.

---

## History

This project is designed to be minimalist, cross-platform, and 100% based on Python’s standard library.
