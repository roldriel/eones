# Contributing to Eones

First of all, thank you for your interest in contributing to **Eones** — a minimalist, expressive and dependency-free date/time library for Python.

This project values **clarity, correctness, and composability** over feature-bloat or excessive abstraction. Contributions are welcome, as long as they align with these principles.

---

## 🧭 Guiding Principles

- **Standard Library only**: Avoid adding external dependencies.
- **Strong typing**: All public interfaces must be type hinted using `mypy`-compatible syntax.
- **Black + Pylint compliance**: Run formatting and linting before submitting a pull request.
- **Explicit over implicit**: Prefer readable code over clever hacks.
- **UTC by default**: Timezone handling must be safe, predictable, and always explicit.

---

## 🛠 Setup

To contribute, clone the repository and install the dev dependencies:

```bash
git clone https://github.com/your-username/eones.git
cd eones
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
```

---

## 🧪 Running Tests

Eones uses `pytest`. To run all tests:

```bash
pytest
```

To check coverage:

```bash
pytest --cov=src/eones --cov-report=term-missing
```

To run linters:

```bash
black src tests
pylint src/eones
```

---

## ✍️ Pull Request Guidelines

- Each PR should focus on a **single concern**.
- Include or update **unit tests** for any change in logic.
- Add or improve **docstrings** in public APIs.
- If fixing a bug, include a minimal test case to reproduce the issue.
- If adding a feature, explain the motivation and provide an example of usage.

---

## 📄 File Structure

```
src/eones/           # Core logic: date, delta, parser, range
tests/               # Pytest-based unit tests
docs/                # Sphinx documentation (optional)
```

---

## 💬 Need Help?

Feel free to open a [Discussion](https://github.com/roldriel/eones/discussions) or reach out via issues.

Thanks again for contributing to Eones 🙌
