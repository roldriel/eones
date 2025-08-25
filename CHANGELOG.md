# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changes since v1.3.0

## [1.3.0] - 2025-08-25

### Added
- New range utilities ([25d1d79](https://github.com/roldriel/eones/commit/25d1d79))
- Delta utility properties and constructors ([c8dffd9](https://github.com/roldriel/eones/commit/c8dffd9))
- Support for delta in `__add__` and `__sub__` operations ([6252687](https://github.com/roldriel/eones/commit/6252687))

### Fixed
- Removed duplicate function ([77cddba](https://github.com/roldriel/eones/commit/77cddba))

### Changed
- Updated documentation and added new examples ([e41ffcc](https://github.com/roldriel/eones/commit/e41ffcc))
- Updated main README and Spanish README ([bc12e9a](https://github.com/roldriel/eones/commit/bc12e9a))
- Refactored examples and added Spanish language examples ([1325dad](https://github.com/roldriel/eones/commit/1325dad))
- Updated tests with isort and black formatting ([3f1d623](https://github.com/roldriel/eones/commit/3f1d623))
- Minor performance improvements in modules ([4c4058e](https://github.com/roldriel/eones/commit/4c4058e))
- Updated Python configuration versions ([b6f5465](https://github.com/roldriel/eones/commit/b6f5465))
- Updated workflow configurations ([9f9b94c](https://github.com/roldriel/eones/commit/9f9b94c))

### Removed
- Removed old tests and updated config.py, README.es ([7d7c101](https://github.com/roldriel/eones/commit/7d7c101))

### Documentation
- Added AGENTS.md and updated README.es.md ([5a5c2de](https://github.com/roldriel/eones/commit/5a5c2de))
- Documented new error classes ([b118cab](https://github.com/roldriel/eones/commit/b118cab))

### Tests
- Added unit tests and integration tests ([e932f5f](https://github.com/roldriel/eones/commit/e932f5f))
- Added edge case testing ([789856b](https://github.com/roldriel/eones/commit/789856b))


---

## [1.2.0] - 2025-06-25

### Added
- Locale-aware `diff_for_humans` via the new `humanize` module
- `eones/locales/` package for language messages
- Comparison helpers: `Date.is_same_day`, `Date.is_before`, `Date.is_after` and `Date.days_until`
- `Date.as_local` property for local timezone conversion

### Changed
- Exposed `diff_for_humans` on `Date` and `Eones` classes
- Renamed timezone conversion method to `as_zone`
- Integration tests now skip if Django or SQLAlchemy are not installed

### Documentation
- Documented language extensibility and added comprehensive tests

---

## [1.1.0] - 2025-06-13

### Added
- Docstrings to all methods and classes in source code and tests
- Comprehensive tests for all methods and classes
- Methods for handling ranges and periods
- Test coverage reaching 99%

### Changed
- Updated `pyproject.toml` to version 1.1.0
- Updated `README.md` to version 1.1.0

### Fixed
- Bugs in comparison methods

### Known Issues
- Some bugs identified for future fixes

---

## [1.0.0] - 2025-05-19

### Added
- First stable release of the `eones` library
- Unified parser for `str`, `dict`, and `datetime` objects
- Timezone support using `ZoneInfo`
- Truncation, aggregation, comparison, and range methods
- Optional integrations for Django, SQLAlchemy, and serializers
- Centralized interface using the `Eones` class

### Project Goals
- Minimalist design philosophy
- Cross-platform compatibility
- 100% based on Python's standard library
