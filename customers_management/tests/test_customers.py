from flask_jwt_extended import create_access_token
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from customers_management.src.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'qwerty'
    with app.test_client() as client:
        yield client

def test_ping(client):
    response = client.get('/customers/ping')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'pong'}

@patch('customers_management.src.api.customers.GetCustomers')
def test_get_customers_success(mock_get_customers, client):
    mock_execute = MagicMock(return_value=(jsonify([{'firstName': 'Carlos'}]), 200))
    
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    mock_get_customers.return_value.execute = mock_execute

    response = client.get('/customers', headers=headers)
    assert response.status_code == 200
    assert response.get_json() == [{'firstName': 'Carlos'}]
    mock_execute.assert_called_once()


@patch('customers_management.src.api.customers.GetCustomers')
def test_get_customers_exception(mock_get_customers, client):
    mock_get_customers.return_value.execute.side_effect = Exception("DB Error")

    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get('/customers', headers=headers)
    assert response.status_code == 500
    assert response.get_json() == {'error': 'DB Error'}
    
@patch('customers_management.src.api.customers.SyncCustomer')
def test_sync_customer_success(mock_sync_customer, client):
    mock_execute = MagicMock(return_value={'message': 'Customer synced successfully'})
    mock_sync_customer.return_value.execute = mock_execute

    response = client.post('/customers/sync', json={"id": "123"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Customer synced successfully'}
    mock_execute.assert_called_once()

@patch('customers_management.src.api.customers.SyncCustomer')
def test_sync_customer_with_error(mock_sync_customer, client):
    mock_execute = MagicMock(return_value={'error': 'Invalid data'})
    mock_sync_customer.return_value.execute = mock_execute

    response = client.post('/customers/sync', json={"id": "invalid"})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid data'}
    mock_execute.assert_called_once()

@patch('customers_management.src.api.customers.SyncCustomer')
def test_sync_customer_exception(mock_sync_customer, client):
    mock_sync_customer.return_value.execute.side_effect = Exception("Unexpected error")

    response = client.post('/customers/sync', json={"id": "123"})
    assert response.status_code == 500
    assert response.get_json() == {'error': 'Unexpected error'}
