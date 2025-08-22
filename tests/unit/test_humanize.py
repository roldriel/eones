"""Tests for humanize module."""

import pytest

from eones.core.date import Date
from eones.humanize import diff_for_humans


def test_diff_for_humans_with_none_other():
    """Test diff_for_humans with other=None (lines 27-29)."""
    # Test the case where other=None, which should create Date.now() internally
    # Use a date close to now to get "just now" result
    date1 = Date.now(tz="UTC", naive="utc")
    result = diff_for_humans(date1, other=None)
    assert isinstance(result, str)
    assert "just now" in result


def test_diff_for_humans_just_now_case():
    """Test diff_for_humans just_now case (line 50)."""
    date1 = Date.now(tz="UTC", naive="utc")
    date2 = Date.now(tz="UTC", naive="utc")
    result = diff_for_humans(date1, date2)
    assert "just now" in result
