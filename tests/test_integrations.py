"""tests.test_integrations.py"""

import pytest


def test_import_django():
    pytest.importorskip("django")
    import eones.integrations.django


def test_import_serializers():
    import eones.integrations.serializers


def test_import_sqlalchemy():
    pytest.importorskip("sqlalchemy")
    import eones.integrations.sqlalchemy
