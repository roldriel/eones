# Contribuir a Eones

Primero que nada, ¡gracias por tu interés en contribuir a **Eones**! Esta es una librería minimalista, expresiva y sin dependencias externas para manejar fechas y tiempos en Python.

Este proyecto valora la **claridad, corrección y composabilidad** por sobre la sobreabundancia de funcionalidades o la abstracción excesiva. Las contribuciones son bienvenidas, siempre que se alineen con estos principios.

---

## 🧭 Principios Guía

- **Solo biblioteca estándar**: Evitá agregar dependencias externas.
- **Tipado fuerte**: Todas las interfaces públicas deben usar anotaciones de tipo compatibles con `mypy`.
- **Cumplimiento con Black + Pylint**: Ejecutá formateo y linting antes de enviar un pull request.
- **Explícito mejor que implícito**: Preferimos código legible por sobre trucos ingeniosos.
- **UTC por defecto**: El manejo de zonas horarias debe ser seguro, predecible y siempre explícito.

---

## 🛠 Configuración del Entorno

Para contribuir, cloná el repositorio e instalá las dependencias de desarrollo:

```bash
git clone https://github.com/roldriel/eones.git
cd eones
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements-dev.txt
```

---

## 🧪 Ejecutar Tests

Eones usa `pytest`. Para correr todos los tests:

```bash
pytest
```

Para verificar la cobertura:

```bash
pytest --cov=src/eones --cov-report=term-missing
```

Para ejecutar los linters:

```bash
black src tests
pylint src/eones
```

---

## ✍️ Guía para Pull Requests

- Cada PR debe enfocarse en **un solo objetivo**.
- Incluí o actualizá **tests unitarios** para cualquier cambio en la lógica.
- Agregá o mejorá los **docstrings** en las APIs públicas.
- Si estás corrigiendo un bug, incluí un caso mínimo que lo reproduzca.
- Si estás agregando una funcionalidad, explicá la motivación e incluí un ejemplo de uso.

---

## 📄 Estructura del Proyecto

```
src/eones/           # Lógica central: date, delta, parser, range
tests/               # Tests unitarios con pytest
docs/                # Documentación con Sphinx (opcional)
```

---

## 💬 ¿Necesitás ayuda?

Podés abrir una [Discusión](https://github.com/roldriel/eones/discussions) o dejar tu consulta en un issue.

¡Gracias nuevamente por contribuir a Eones 🙌!
