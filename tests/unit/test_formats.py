from eones import Eones


def test_is_valid_format_success():
    formats = ["%Y-%m-%d", "%d/%m/%Y"]
    assert Eones.is_valid_format("2025-06-15", formats)
    assert Eones.is_valid_format("15/06/2025", formats)


def test_is_valid_format_failure():
    formats = ["%Y-%m-%d"]
    assert not Eones.is_valid_format("15-06-2025", formats)


def test_sanitize_formats():
    formats = ["%Y-%m-%d", "%Y-%m-%d", "%d/%m/%Y", 123, None]
    result = Eones.sanitize_formats(formats)
    assert "%Y-%m-%d" in result
    assert "%d/%m/%Y" in result
    assert all(isinstance(fmt, str) for fmt in result)


def test_add_days_to_date():
    z = Eones("2025-05-15")
    z.add(days=5)
    assert z.format("%Y-%m-%d") == "2025-05-20"


def test_add_months_to_date():
    z = Eones("2025-01-31")
    z.add(months=1)
    assert z.format("%Y-%m-%d") == "2025-02-28"  # manejo de mes corto


def test_format_date():
    z = Eones("2025-12-24")
    formatted = z.format("%d/%m/%Y")
    assert formatted == "24/12/2025"


# ==== Coverage Tests ====


def test_is_valid_format_valid():
    """Test is_valid_format with valid format."""
    from eones.formats import is_valid_format

    result = is_valid_format("2023-01-01", ["%Y-%m-%d"])
    assert result is True


def test_is_valid_format_invalid():
    """Test is_valid_format with invalid format."""
    from eones.formats import is_valid_format

    result = is_valid_format("invalid-date", ["%Y-%m-%d"])
    assert result is False


def test_is_valid_format_multiple_formats():
    """Test is_valid_format with multiple formats."""
    from eones.formats import is_valid_format

    result = is_valid_format("01/01/2023", ["%Y-%m-%d", "%m/%d/%Y"])
    assert result is True


def test_sanitize_formats_with_duplicates():
    """Test sanitize_formats removes duplicates."""
    from eones.formats import sanitize_formats

    formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%d"]
    result = sanitize_formats(formats)
    assert len(result) == 2
    assert "%Y-%m-%d" in result
    assert "%m/%d/%Y" in result


def test_sanitize_formats_with_non_strings():
    """Test sanitize_formats filters non-strings."""
    from eones.formats import sanitize_formats

    formats = ["%Y-%m-%d", 123, None, "%m/%d/%Y", []]
    result = sanitize_formats(formats)
    assert len(result) == 2
    assert "%Y-%m-%d" in result
    assert "%m/%d/%Y" in result
    assert 123 not in result
    assert None not in result
