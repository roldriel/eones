# 📦 CHANGELOG

All versions are documented in this file.

## [Unreleased]
### Cambios desde v1.2.0

### Features
- Add new range utilities ([25d1d79](https://github.com/rolda/eones/commit/25d1d79))
- add delta utility properties and constructors ([c8dffd9](https://github.com/rolda/eones/commit/c8dffd9))
- add support for delta in __add__ & __sub__ ([6252687](https://github.com/rolda/eones/commit/6252687))

### Bug Fixes
- remove duplicate function ([77cddba](https://github.com/rolda/eones/commit/77cddba))

### Documentation
- Update docs, add new examples ([e41ffcc](https://github.com/rolda/eones/commit/e41ffcc))
- update main Readme and spanish readme ([bc12e9a](https://github.com/rolda/eones/commit/bc12e9a))
- remove old tests, update config.py, update README.es ([7d7c101](https://github.com/rolda/eones/commit/7d7c101))
- Add AGENTS.md, update README.es.md ([5a5c2de](https://github.com/rolda/eones/commit/5a5c2de))

### Refactoring
- changes on examples, add examples lang es ([1325dad](https://github.com/rolda/eones/commit/1325dad))

### Tests
- update tests, apply isort, black ([3f1d623](https://github.com/rolda/eones/commit/3f1d623))
- add unit tests & integration test ([e932f5f](https://github.com/rolda/eones/commit/e932f5f))
- add edge cases ([789856b](https://github.com/rolda/eones/commit/789856b))

### Performance
- minor changes on some modules ([4c4058e](https://github.com/rolda/eones/commit/4c4058e))
- Document new error classes ([b118cab](https://github.com/rolda/eones/commit/b118cab))

### CI/CD
- update missing python configuration versions ([b6f5465](https://github.com/rolda/eones/commit/b6f5465))
- update config on workflows ([9f9b94c](https://github.com/rolda/eones/commit/9f9b94c))


---

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
