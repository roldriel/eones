# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changes since v1.3.6

## [1.3.6] - 2025-01-19

### Fixed
- Resolved context access warnings in GitHub Actions workflows ([13069b4](https://github.com/roldriel/eones/commit/13069b4))
- Fixed nested quotes syntax error in release workflow commit message
- Added conditional checks for job outputs to prevent invalid context access

### Changed
- Updated version to 1.3.6 across all project files
- Improved workflow robustness with fallback values for tag and version outputs

## [1.3.5] - 2025-01-17

### Fixed
- Updated example links to full GitHub URLs for PyPI compatibility
- Fixed broken relative links in README files when displayed on PyPI

### Changed
- Updated version to 1.3.5 across all project files ([0a2a63e](https://github.com/roldriel/eones/commit/0a2a63e))
- Improved documentation accessibility on PyPI

## [1.3.3] - 2025-08-26

### Fixed
- Correct import formatting errors detected by isort ([19752e6](https://github.com/roldriel/eones/commit/19752e6))

### Changed
- Updated version to 1.3.3
- Improved code quality and formatting consistency

## [1.3.2] - 2025-08-25

### Changed
- Version bump for development ([652c2ac](https://github.com/roldriel/eones/commit/652c2ac))

## [1.3.1] - 2025-08-25

### Fixed
- Add missing is_valid_format static method to Eones class
- Fix import-outside-toplevel pylint warning
- Fix docstring syntax error

### Changed
- Update git-cliff-action from v2 to v3 for better stability
- Add OUTPUT environment variable to release workflow
- Version bump to 1.3.1 ([288752f](https://github.com/roldriel/eones/commit/288752f))

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
