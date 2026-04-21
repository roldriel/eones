"""tests/unit/test_humanize.py"""

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


@pytest.mark.parametrize(
    "locale, past_prefix, future_prefix, day_singular, day_plural, just_now",
    [
        ("en", "ago", "in", "day", "days", "just now"),
        ("es", "hace", "en", "día", "días", "ahora mismo"),
        ("fr", "il y a", "dans", "jour", "jours", "à l'instant"),
        ("de", "vor", "in", "Tag", "Tagen", "gerade eben"),
        ("ja", "前", "後", "日", "日", "たった今"),
    ],
)
def test_diff_for_humans_locale(
    locale, past_prefix, future_prefix, day_singular, day_plural, just_now
):
    """Test diff_for_humans with all supported locales."""
    from datetime import timedelta

    now = Date.now(tz="UTC", naive="utc")
    yesterday = now.shift(timedelta(days=-1))
    tomorrow = now.shift(timedelta(days=1))
    three_days_ago = now.shift(timedelta(days=-3))

    past_result = diff_for_humans(yesterday, now, locale=locale)
    assert day_singular in past_result
    assert past_prefix in past_result

    future_result = diff_for_humans(tomorrow, now, locale=locale)
    assert day_singular in future_result
    assert future_prefix in future_result

    plural_result = diff_for_humans(three_days_ago, now, locale=locale)
    assert day_plural in plural_result

    just_now_result = diff_for_humans(now, now, locale=locale)
    assert just_now_result == just_now


class TestJapaneseSuffixPosition:
    """Tests for Japanese suffix position formatting."""

    def test_past_suffix_no_space_before_marker(self):
        """Test that past uses suffix pattern without space before marker."""
        from datetime import timedelta

        now = Date.now(tz="UTC", naive="utc")
        two_days_ago = now.shift(timedelta(days=-2))
        result = diff_for_humans(two_days_ago, now, locale="ja")
        assert result == "2 日前"

    def test_future_suffix_no_space_before_marker(self):
        """Test that future uses suffix pattern without space before marker."""
        from datetime import timedelta

        now = Date.now(tz="UTC", naive="utc")
        two_days_later = now.shift(timedelta(days=2))
        result = diff_for_humans(two_days_later, now, locale="ja")
        assert result == "2 日後"

    def test_past_hours(self):
        """Test Japanese past with hours."""
        from datetime import timedelta

        now = Date.now(tz="UTC", naive="utc")
        three_hours_ago = now.shift(timedelta(hours=-3))
        result = diff_for_humans(three_hours_ago, now, locale="ja")
        assert result == "3 時間前"

    def test_future_weeks(self):
        """Test Japanese future with weeks."""
        from datetime import timedelta

        now = Date.now(tz="UTC", naive="utc")
        two_weeks_later = now.shift(timedelta(weeks=2))
        result = diff_for_humans(two_weeks_later, now, locale="ja")
        assert result == "2 週間後"

    def test_singular_year(self):
        """Test Japanese with singular year (no plural distinction)."""
        from datetime import timedelta

        now = Date.now(tz="UTC", naive="utc")
        one_year_ago = now.shift(timedelta(days=-366))
        result = diff_for_humans(one_year_ago, now, locale="ja")
        assert result == "1 年前"
