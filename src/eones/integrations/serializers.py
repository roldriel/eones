def eones_encoder(obj):
    """Generic JSON encoder for EonesDate."""
    from eones.core.date import EonesDate

    if isinstance(obj, EonesDate):
        return obj.to_iso()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
