import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import patch
from authentications_management.src.main import app
from authentications_management.src.models.database import db_session
from authentications_management.src.errors.errors import (
    InvalidData,
    EmailDoesNotValid,
    UserAlreadyExists,
    InvalidIdentification,
    InvalidName,
    InvalidCountry,
    InvalidAddress,
    InvalidTelephone,
    InvalidEmail,
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'qwerty'
    with app.test_client() as client:
        yield client


@patch('authentications_management.src.commands.create_users.CreateUsers.execute')
def test_create_users_success(mock_create_users, client):
    mock_create_users.return_value = {'message': 'Usuario enviado a la cola exitosamente'}
    response = client.post('/users', json={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
        'role': 'CLIENTE'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Usuario enviado a la cola exitosamente'

def test_create_users_invalid_data(client):
    response = client.post('/users', json={})
    assert response.status_code == 400


@patch('authentications_management.src.commands.login_user.LoginUserCommand.execute')
def test_login_success(mock_login, client):
    mock_login.return_value = {'token': 'fake-jwt-token'}
    response = client.post('/users/login', json={
        'email': 'test@example.com',
        'password': 'Test1234!'
    })
    assert response.status_code == 200
    assert 'token' in response.json

def test_login_invalid_data(client):
    response = client.post('/users/login', json={})
    assert response.status_code == 400


@patch('authentications_management.src.commands.create_customer.CreateCustomer.execute')
def test_create_customers_success(mock_create_customer, client):
    mock_create_customer.return_value = {'message': 'Customer created successfully'}
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/customers', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'country': 'USA',
        'address': '123 Main St',
        'phoneNumber': '+12345678901',
        'email': 'john.doe@example.com'
    }, headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Customer created successfully'

def test_create_customers_invalid_data(client):
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/customers', json={}, headers=headers)
    assert response.status_code == 400

@patch('authentications_management.src.commands.create_customer.CreateCustomer.execute')
def test_create_customers_email_not_valid(mock_create_customer, client):
    mock_create_customer.side_effect = EmailDoesNotValid()
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/customers', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'country': 'USA',
        'address': '123 Main St',
        'phoneNumber': '+12345678901',
        'email': 'bad-email'
    }, headers=headers)
    assert response.status_code == 400

@patch('authentications_management.src.commands.create_customer.CreateCustomer.execute')
def test_create_customers_user_already_exists(mock_create_customer, client):
    mock_create_customer.side_effect = UserAlreadyExists()
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/customers', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'country': 'USA',
        'address': '123 Main St',
        'phoneNumber': '+12345678901',
        'email': 'existing@example.com'
    }, headers=headers)
    assert response.status_code == 409

@patch('authentications_management.src.commands.create_customer.CreateCustomer.execute')
def test_create_customers_unexpected_error(mock_create_customer, client):
    mock_create_customer.side_effect = Exception("DB error")
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/customers', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'country': 'USA',
        'address': '123 Main St',
        'phoneNumber': '+12345678901',
        'email': 'error@example.com'
    }, headers=headers)
    assert response.status_code == 500
    assert 'unexpected' in response.json['error']


@patch('authentications_management.src.commands.create_sellers.CreateSellers.execute')
def test_create_sellers_success(mock_create_sellers, client):
    mock_create_sellers.return_value = {'message': 'Seller has been created successfully'}
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/sellers', json={
        'identification': '123456',
        'name': 'Seller Name',
        'country': 'USA',
        'address': '123 Main St',
        'telephone': '1234567890',
        'email': 'seller@example.com'
    }, headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Seller has been created successfully'

@pytest.mark.parametrize("error_class", [
    InvalidIdentification, InvalidName, InvalidCountry,
    InvalidAddress, InvalidTelephone, InvalidEmail
])
@patch('authentications_management.src.commands.create_sellers.CreateSellers.execute')
def test_create_sellers_errors(mock_create_sellers, client, error_class):
    mock_create_sellers.side_effect = error_class()
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/sellers', json={
        'identification': '123456',
        'name': 'Invalid Seller',
        'country': 'Nowhere',
        'address': '123',
        'telephone': '000',
        'email': 'bademail'
    }, headers=headers)
    assert response.status_code == 400


def test_ping(client):
    response = client.get('/users/ping')
    assert response.status_code == 200
    assert response.json['message'] == 'pong'
