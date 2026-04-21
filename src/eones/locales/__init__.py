"""src/eones/locales/__init__.py"""

from __future__ import annotations

from functools import lru_cache
from importlib import import_module
from typing import Dict, Tuple, Union, cast

DEFAULT_LOCALE = "en"


@lru_cache(maxsize=None)
def get_messages(locale: str) -> Dict[str, Union[str, Tuple[str, str]]]:
    """Load locale messages dynamically from ``eones.locales`` modules.

    Falls back to English if the given locale is not available.
    """
    try:
        module = import_module(f"eones.locales.{locale}")

    except ModuleNotFoundError:
        module = import_module(f"eones.locales.{DEFAULT_LOCALE}")

    return cast(Dict[str, Union[str, Tuple[str, str]]], getattr(module, "MESSAGES"))


@lru_cache(maxsize=None)
def get_locale_data(locale: str) -> Dict[str, Tuple[str, ...]]:
    """Load complete locale data (MONTHS, MONTHS_SHORT, DAYS, DAYS_SHORT).

    Falls back to English if the given locale is not available.

    Args:
        locale: Two-letter language code.

    Returns:
        Dictionary with ``months``, ``months_short``, ``days`` and
        ``days_short`` tuples.
    """
    try:
        module = import_module(f"eones.locales.{locale}")
    except ModuleNotFoundError:
        module = import_module(f"eones.locales.{DEFAULT_LOCALE}")

    fallback = import_module(f"eones.locales.{DEFAULT_LOCALE}")

    return {
        "months": getattr(module, "MONTHS", getattr(fallback, "MONTHS")),
        "months_short": getattr(
            module, "MONTHS_SHORT", getattr(fallback, "MONTHS_SHORT")
        ),
        "days": getattr(module, "DAYS", getattr(fallback, "DAYS")),
        "days_short": getattr(module, "DAYS_SHORT", getattr(fallback, "DAYS_SHORT")),
    }
