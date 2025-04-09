import pytest
from authentications_management.src.main import app, init_db
from authentications_management.src.models.database import db_session, base
from authentications_management.src.models.users import Users, Role

@pytest.fixture
def client():
    app.config.from_object('authentications_management.tests.conftest')
    with app.test_client() as client:
        with app.app_context():
            base.metadata.create_all(bind=db_session.bind)
        yield client
        with app.app_context():
            base.metadata.drop_all(bind=db_session.bind)

@pytest.fixture
def setup_user():
    user = Users(email='test@example.com', password='Test1234!', role=Role.Administrador)
    db_session.add(user)
    db_session.commit()
    yield user
    db_session.remove()

def test_login_success(client, setup_user):
    response = client.post('/users/login', json={
        'email': 'test@example.com',
        'password': 'Test1234!'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_login_invalid_password(client, setup_user):
    response = client.post('/users/login', json={
        'email': 'test@example.com',
        'password': 'WrongPassword!'
    })
    assert response.status_code == 401
    assert 'Contraseña inválida' in response.json['mssg']

def test_login_user_not_found(client):
    response = client.post('/users/login', json={
        'email': 'nonexistent@example.com',
        'password': 'Test1234!'
    })
    assert response.status_code == 404
    assert 'Usuario no encontrado' in response.json['mssg']
