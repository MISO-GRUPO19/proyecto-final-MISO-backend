import pytest
from unittest import mock
from ..src.models.database import init_db, base

def test_init_db(monkeypatch):
    monkeypatch.setattr(base.metadata, 'create_all', mock.Mock())
    init_db()
    assert True