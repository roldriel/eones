"""errors.py"""


class EonesError(Exception):
    """Base exception class for all Eones errors."""


class InvalidDateError(EonesError):
    """Raised when a provided date is invalid or cannot be parsed."""

    def __init__(self, message: str = "Invalid date format or value") -> None:
        """Initialize InvalidDateError with a custom message."""
        super().__init__(message)


class InvalidFormatError(EonesError):
    """Raised when an invalid or unsupported format string is used."""

    def __init__(self, message: str = "Invalid or unsupported date format") -> None:
        """Initialize InvalidFormatError with a custom message."""
        super().__init__(message)


class InvalidTimezoneError(EonesError):
    """Raised when an invalid timezone string is provided."""

    def __init__(self, tz: str) -> None:
        """Initialize InvalidTimezoneError with the problematic timezone."""
        super().__init__(f"Invalid timezone: {tz}")


class UnsupportedInputError(EonesError):
    """Raised when the input type is not supported by the parser."""

    def __init__(
        self, message: str = "Unsupported input type for date parsing"
    ) -> None:
        """Initialize UnsupportedInputError with a custom message."""
        super().__init__(message)
