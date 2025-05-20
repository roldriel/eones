import pytest

from eones.errors import (
    EonesError,
    InvalidDateError,
    InvalidFormatError,
    UnsupportedInputError,
)


def test_eones_error_is_base():
    with pytest.raises(EonesError):
        raise EonesError("Generic error")


def test_invalid_date_error():
    with pytest.raises(InvalidDateError) as exc_info:
        raise InvalidDateError("Bad date")
    assert "Bad date" in str(exc_info.value)


def test_invalid_format_error():
    with pytest.raises(InvalidFormatError) as exc_info:
        raise InvalidFormatError("Format not supported")
    assert "Format not supported" in str(exc_info.value)


def test_unsupported_input_error():
    with pytest.raises(UnsupportedInputError) as exc_info:
        raise UnsupportedInputError("This input is wrong")
    assert "This input is wrong" in str(exc_info.value)
