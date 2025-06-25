"""Helpers for loading locale messages used by ``diff_for_humans``."""

from __future__ import annotations

from functools import lru_cache
from importlib import import_module
from typing import Dict

DEFAULT_LOCALE = "en"


@lru_cache(maxsize=None)
def get_messages(locale: str) -> Dict[str, object]:
    """Load locale messages dynamically from ``eones.locales`` modules.

    Falls back to English if the given locale is not available.
    """
    try:
        module = import_module(f"eones.locales.{locale}")

    except ModuleNotFoundError:
        module = import_module(f"eones.locales.{DEFAULT_LOCALE}")

    return getattr(module, "MESSAGES")
