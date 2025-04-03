import pytest
from authentications_management.src.main import app
from authentications_management.src.models.database import db_session, base
from unittest.mock import patch

@pytest.fixture
def test_client():
    app.config.from_object('authentications_management.tests.conftest')
    with app.test_client() as client:
        with app.app_context():
            base.metadata.create_all(bind=db_session.bind)
        yield client
        with app.app_context():
            base.metadata.drop_all(bind=db_session.bind)

@patch('authentications_management.src.pubsub.publisher.pubsub_v1.PublisherClient')
def test_create_user(mock_publisher, test_client):
    mock_publisher.return_value.publish.return_value = None  # Simula la publicación

    response = test_client.post('/users', json={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
        'role': 1
    })
    assert response.status_code == 201
    assert 'Usuario creado exitosamente' in response.json['message']

def test_create_user_invalid_email(test_client):
    response = test_client.post('/users', json={
        'email': 'invalid-email',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
        'role': 'CLIENTE'
    })
    assert response.status_code == 400
    assert 'Datos inválidos' in response.json['mssg']

def test_create_user_password_mismatch(test_client):
    response = test_client.post('/users', json={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test12345!',
        'role': 'CLIENTE'
    })
    assert response.status_code == 400
    assert 'Confirmación de contraseña no coincide' in response.json['mssg']

def test_create_user_invalid_role(test_client):
    response = test_client.post('/users', json={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
        'role': 'INVALID_ROLE'
    })
    assert response.status_code == 400
    assert 'Datos inválidos' in response.json['mssg']

def test_ping(test_client):
    response = test_client.get('/users/ping')
    assert response.status_code == 200
    assert 'pong' in response.json['message']
