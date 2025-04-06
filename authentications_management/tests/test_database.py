import pytest
from unittest import mock
from authentications_management.src.models.database import init_db, db_session, base
from authentications_management.src.models.users import Users, Role

def test_init_db(monkeypatch):
    monkeypatch.setattr(base.metadata, 'create_all', mock.Mock())
    init_db()
    assert True
