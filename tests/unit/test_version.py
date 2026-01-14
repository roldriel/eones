"""tests/unit/test_version.py"""

import eones


def test_version():
    assert isinstance(eones.__version__, str)
    assert len(eones.__version__) > 0
