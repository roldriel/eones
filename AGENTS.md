# Codex Agent Instructions for Eones

This repository contains the **Eones** library – a minimalist date/time manipulation package written in Python 3.9+. All source code lives under `src/eones/` and the tests are in `tests/`.

## Development Principles
- Only use Python's **standard library**. External dependencies are discouraged (see "Standard Library only" in CONTRIBUTING.md). The optional `tzdata` package is the only extra dependency mentioned in the README.
- Maintain **strong typing** for all public interfaces using `mypy` compatible annotations.
- Code must comply with **Black** formatting and **Pylint** linting.
- Prefer readability and explicit behavior; timezone handling should default to UTC.

Relevant lines in `CONTRIBUTING.md` include:
```
- **Standard Library only**: Avoid adding external dependencies.
- **Strong typing**: All public interfaces must be type hinted using `mypy`-compatible syntax.
- **Black + Pylint compliance**: Run formatting and linting before submitting a pull request.
- **Explicit over implicit**: Prefer readable code over clever hacks.
- **UTC by default**: Timezone handling must be safe, predictable, and always explicit.
```

## Project Structure
```
src/eones/           # Core logic: date, delta, parser, range
tests/               # Pytest-based unit tests
docs/                # Sphinx documentation (optional)
```
(The above is excerpted from `CONTRIBUTING.md`.)

## Checks Before Commit
Run the following commands before committing any change:
```bash
black --check src tests
pylint src/eones
pytest
```
These commands are derived from the "Running Tests" and "To run linters" sections of `CONTRIBUTING.md`.

## Pull Request Guidelines
- Each PR should focus on a single concern.
- Include or update unit tests for any logic changes.
- Add or improve docstrings in public APIs.
- Provide a minimal reproducible test case when fixing bugs.
- Explain motivation and usage examples when adding features.

Following these guidelines helps maintain consistency and allows Codex to analyze and modify the repository effectively.