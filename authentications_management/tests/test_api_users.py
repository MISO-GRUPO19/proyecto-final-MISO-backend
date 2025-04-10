import pytest
from unittest.mock import patch, MagicMock
from authentications_management.src.main import app
from authentications_management.src.models.database import db_session

@pytest.fixture
def client():
    app.config['TESTING'] = True
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

@patch('authentications_management.src.commands.create_customer.CreateCustomer.execute')
def test_create_customers_success(mock_create_customer, client):
    mock_create_customer.return_value = {'message': 'Customer created successfully'}
    response = client.post('/users/customers', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'country': 'USA',
        'address': '123 Main St',
        'phoneNumber': '+12345678901',
        'email': 'john.doe@example.com'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Customer created successfully'

@patch('authentications_management.src.commands.create_sellers.CreateSellers.execute')
def test_create_sellers_success(mock_create_sellers, client):
    mock_create_sellers.return_value = {'message': 'Seller has been created successfully'}
    
    headers = {
        'Authorization': 'Bearer fake-valid-token'
    }
    
    response = client.post('/users/sellers', json={
        'identification': '123456',
        'name': 'Seller Name',
        'country': 'USA',
        'address': '123 Main St',
        'telephone': '+12345678901',
        'email': 'seller@example.com'
    }, headers=headers)
    
    assert response.status_code == 201
    assert response.json['message'] == 'Seller has been created successfully'

def test_ping(client):
    response = client.get('/users/ping')
    assert response.status_code == 200
    assert response.json['message'] == 'pong'