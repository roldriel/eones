"""formats.py"""

from datetime import datetime
from typing import List


def is_valid_format(date_str: str, formats: List[str]) -> bool:
    """
    Check if a date string matches any of the provided formats.

    :param date_str: The date string to validate.
    :param formats: A list of accepted datetime format strings.
    :return: True if the string matches at least one format.
    """
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True

        except ValueError:
            continue

    return False


def sanitize_formats(formats: List[str]) -> List[str]:
    """
    Remove duplicates and ensure all formats are strings.

    :param formats: A list of format definitions.
    :return: Cleaned list with unique and valid format strings.
    """
    return list({fmt for fmt in formats if isinstance(fmt, str)})
