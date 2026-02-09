"""src/eones/integrations/serializers.py"""

from __future__ import annotations

from typing import Any

from eones.core.date import Date
from eones.core.delta import Delta
from eones.interface import Eones


def eones_encoder(obj: Any) -> Any:
    """JSON encoder for Eones, Date and Delta objects.

    Intended for use as the ``default`` argument of ``json.dumps``::

        json.dumps(data, default=eones_encoder)

    Args:
        obj: The object to serialize.

    Returns:
        An ISO 8601 string representation.

    Raises:
        TypeError: If the object is not a supported Eones type.
    """

    if isinstance(obj, Eones):
        return obj.for_json()
    if isinstance(obj, Date):
        return obj.to_iso()
    if isinstance(obj, Delta):
        return obj.to_iso()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
