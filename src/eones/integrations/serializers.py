"""src/eones/integrations/serializers.py"""

from typing import Any


def eones_encoder(obj: Any) -> Any:
    """Generic JSON encoder for Date."""
    from eones.core.date import Date

    if isinstance(obj, Date):
        return obj.to_iso()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
