import pytest
from unittest import mock
from authentications_management.src.models.database import init_db, db_session, base
from authentications_management.src.models.users import Users, Role

def test_init_db(monkeypatch):
    monkeypatch.setattr(base.metadata, 'create_all', mock.Mock())
    init_db()
    assert True

def test_db_session():
    user = Users(email='test@example.com', password='password123', role=Role.Cliente)
    db_session.add(user)
    db_session.commit()
    retrieved_user = db_session.query(Users).filter_by(email='test@example.com').first()
    assert retrieved_user is not None
    assert retrieved_user.email == 'test@example.com'