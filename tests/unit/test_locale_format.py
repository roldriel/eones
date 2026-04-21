"""tests/unit/test_locale_format.py"""

import pytest

from eones.locale_format import format_locale


class TestFormatLocaleMonths:
    """Tests for MMMM and MMM tokens."""

    @pytest.mark.parametrize(
        "locale, month, expected_full, expected_short",
        [
            ("en", 1, "January", "Jan"),
            ("en", 6, "June", "Jun"),
            ("en", 12, "December", "Dec"),
            ("es", 1, "enero", "ene"),
            ("es", 5, "mayo", "may"),
            ("es", 12, "diciembre", "dic"),
            ("fr", 3, "mars", "mar"),
            ("fr", 8, "août", "aoû"),
            ("de", 3, "März", "Mär"),
            ("de", 10, "Oktober", "Okt"),
            ("ja", 1, "1月", "1月"),
            ("ja", 12, "12月", "12月"),
        ],
    )
    def test_month_names(self, locale, month, expected_full, expected_short):
        """Test full and abbreviated month names across locales."""
        result_full = format_locale(2026, month, 15, 0, 0, 0, 0, "MMMM", locale)
        assert result_full == expected_full

        result_short = format_locale(2026, month, 15, 0, 0, 0, 0, "MMM", locale)
        assert result_short == expected_short


class TestFormatLocaleDays:
    """Tests for dddd and ddd tokens."""

    @pytest.mark.parametrize(
        "locale, weekday, expected_full, expected_short",
        [
            ("en", 0, "Monday", "Mon"),
            ("en", 6, "Sunday", "Sun"),
            ("es", 0, "lunes", "lun"),
            ("es", 4, "viernes", "vie"),
            ("fr", 2, "mercredi", "mer"),
            ("de", 0, "Montag", "Mo"),
            ("de", 4, "Freitag", "Fr"),
            ("ja", 0, "月曜日", "月"),
            ("ja", 6, "日曜日", "日"),
        ],
    )
    def test_day_names(self, locale, weekday, expected_full, expected_short):
        """Test full and abbreviated day names across locales."""
        result_full = format_locale(2026, 1, 1, weekday, 0, 0, 0, "dddd", locale)
        assert result_full == expected_full

        result_short = format_locale(2026, 1, 1, weekday, 0, 0, 0, "ddd", locale)
        assert result_short == expected_short


class TestFormatLocaleNumericTokens:
    """Tests for numeric tokens DD, D, MM, M, YYYY, YY, HH, mm, ss."""

    def test_dd_zero_padded(self):
        """Test DD produces zero-padded day."""
        assert format_locale(2026, 1, 5, 0, 0, 0, 0, "DD") == "05"
        assert format_locale(2026, 1, 15, 0, 0, 0, 0, "DD") == "15"

    def test_d_no_padding(self):
        """Test D produces unpadded day."""
        assert format_locale(2026, 1, 5, 0, 0, 0, 0, "D") == "5"
        assert format_locale(2026, 1, 15, 0, 0, 0, 0, "D") == "15"

    def test_mm_zero_padded_month(self):
        """Test MM produces zero-padded month number."""
        assert format_locale(2026, 3, 1, 0, 0, 0, 0, "MM") == "03"
        assert format_locale(2026, 12, 1, 0, 0, 0, 0, "MM") == "12"

    def test_m_no_padding_month(self):
        """Test M produces unpadded month number."""
        assert format_locale(2026, 3, 1, 0, 0, 0, 0, "M") == "3"

    def test_yyyy_four_digit_year(self):
        """Test YYYY produces four-digit year."""
        assert format_locale(2026, 1, 1, 0, 0, 0, 0, "YYYY") == "2026"

    def test_yy_two_digit_year(self):
        """Test YY produces two-digit year."""
        assert format_locale(2026, 1, 1, 0, 0, 0, 0, "YY") == "26"
        assert format_locale(2000, 1, 1, 0, 0, 0, 0, "YY") == "00"

    def test_hh_zero_padded_hour(self):
        """Test HH produces zero-padded hour."""
        assert format_locale(2026, 1, 1, 0, 9, 0, 0, "HH") == "09"
        assert format_locale(2026, 1, 1, 0, 14, 0, 0, "HH") == "14"

    def test_mm_zero_padded_minute(self):
        """Test mm produces zero-padded minute."""
        assert format_locale(2026, 1, 1, 0, 0, 5, 0, "mm") == "05"

    def test_ss_zero_padded_second(self):
        """Test ss produces zero-padded second."""
        assert format_locale(2026, 1, 1, 0, 0, 0, 7, "ss") == "07"


class TestFormatLocaleComposite:
    """Tests for composite format strings."""

    def test_spanish_full_date(self):
        """Test composite format with Spanish locale."""
        # 2026-05-25 is a Monday (weekday=0)
        result = format_locale(2026, 5, 25, 0, 0, 0, 0, "DD de MMMM de YYYY", "es")
        assert result == "25 de mayo de 2026"

    def test_spanish_day_and_month(self):
        """Test day name and month name in Spanish."""
        result = format_locale(2026, 5, 25, 0, 0, 0, 0, "dddd DD de MMMM", "es")
        assert result == "lunes 25 de mayo"

    def test_english_full_date(self):
        """Test composite format with English locale."""
        result = format_locale(2026, 5, 25, 0, 0, 0, 0, "dddd, MMMM DD", "en")
        assert result == "Monday, May 25"

    def test_japanese_date(self):
        """Test Japanese date format."""
        result = format_locale(2026, 3, 15, 6, 0, 0, 0, "YYYY年MM月DD日 (ddd)", "ja")
        assert result == "2026年03月15日 (日)"

    def test_french_short_date(self):
        """Test French short format."""
        result = format_locale(2026, 7, 14, 1, 0, 0, 0, "ddd DD MMM YYYY", "fr")
        assert result == "mar 14 jul 2026"

    def test_german_with_time(self):
        """Test German format with time components."""
        result = format_locale(2026, 12, 25, 4, 18, 30, 0, "DD. MMMM YYYY, HH:mm", "de")
        assert result == "25. Dezember 2026, 18:30"

    def test_iso_style_numeric(self):
        """Test purely numeric format (no locale dependency)."""
        result = format_locale(2026, 3, 5, 0, 9, 15, 30, "YYYY-MM-DD HH:mm:ss")
        assert result == "2026-03-05 09:15:30"


class TestFormatLocaleTokenCollision:
    """Tests that longer tokens are replaced before shorter ones."""

    def test_mmmm_not_partially_replaced_by_mmm(self):
        """Test MMMM is not corrupted by MMM replacement."""
        result = format_locale(2026, 1, 1, 0, 0, 0, 0, "MMMM", "en")
        assert result == "January"

    def test_dddd_not_partially_replaced_by_ddd(self):
        """Test dddd is not corrupted by ddd replacement."""
        result = format_locale(2026, 1, 1, 0, 0, 0, 0, "dddd", "en")
        assert result == "Monday"  # weekday 0 = Monday

    def test_mm_not_corrupted_by_m(self):
        """Test MM is not corrupted by M replacement."""
        result = format_locale(2026, 3, 1, 0, 0, 0, 0, "MM", "en")
        assert result == "03"

    def test_dd_not_corrupted_by_d(self):
        """Test DD is not corrupted by D replacement."""
        result = format_locale(2026, 1, 5, 0, 0, 0, 0, "DD", "en")
        assert result == "05"


class TestFormatLocaleFallback:
    """Tests for locale fallback behavior."""

    def test_unknown_locale_falls_back_to_english(self):
        """Test that unknown locale falls back to English."""
        result = format_locale(2026, 1, 1, 0, 0, 0, 0, "MMMM", "xx")
        assert result == "January"
