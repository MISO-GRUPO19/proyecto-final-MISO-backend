import json
from flask import jsonify
import pytest
from faker import Faker
from unittest.mock import patch, MagicMock
from flask_jwt_extended import create_access_token
from orders_management.src.main import app
from uuid import UUID, uuid4
from werkzeug.exceptions import HTTPException
from orders_management.src.errors.errors import InvalidData
fake = Faker()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'qwerty'
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    token = create_access_token(identity=str(uuid4()))
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

@patch('requests.put')
@patch('requests.get')
@patch('orders_management.src.commands.create_orders.CreateOrders.execute')
def test_create_sale_success(mock_execute, mock_requests_get, mock_requests_put, client, auth_headers):
    # Mock the product availability check
    mock_check_response = MagicMock()
    mock_check_response.status_code = 200
    mock_check_response.json.return_value = {"stock_available": True}
    mock_requests_get.return_value = mock_check_response

    # Mock the product stock update
    mock_update_response = MagicMock()
    mock_update_response.status_code = 200
    mock_requests_put.return_value = mock_update_response

    # Mock the order creation
    mock_execute.return_value = jsonify({'message': 'Sale created successfully', 'id': str(uuid4())}), 201

    data = {
        "client_id": str(uuid4()), 
        "seller_id": str(uuid4()),
        "date": fake.date(),
        "provider_id": str(uuid4()),
        "total": round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
        "type": "CLIENTE",
        "route_id": str(uuid4()),
        "products": [{
            "barcode": fake.ean13(),
            "quantity": fake.random_int(min=1, max=10)
        }]
    }

    response = client.post('/orders', data=json.dumps(data), headers=auth_headers)
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['message'] == 'Sale created successfully'
    assert 'id' in response_json

@patch('orders_management.src.commands.create_orders.CreateOrders.execute')
def test_create_sale_missing_fields(mock_execute, client, auth_headers):
    # Change the mock to return a proper error response
    mock_execute.return_value = jsonify({"error": "Invalid data"}), 400

    data = {
        "client_id": str(uuid4()),
        "products": []
    }

    response = client.post('/orders', data=json.dumps(data), headers=auth_headers)
    assert response.status_code == 400

def test_create_sale_no_token(client):
    data = {
        "client_id": str(uuid4()),
        "products": []
    }

    response = client.post('/orders', data=json.dumps(data))
    assert response.status_code == 401

@patch('orders_management.src.queries.get_order_by_client.GetOrderByClient.execute')
def test_get_orders_success(mock_execute, client, auth_headers):
    mock_order = {
        'id': str(uuid4()),
        'products': [],
        'client_id': str(uuid4()),
        'seller_id': str(uuid4()),
        'seller_info': {},
        'date_order': fake.iso8601(),
        'provider_id': str(uuid4()),
        'total': fake.pyfloat(left_digits=3, right_digits=2),
        'type': 'CLIENTE',
        'state': 'pending',
        'route_id': str(uuid4()),
        'status_history': []
    }
    mock_execute.return_value = [mock_order]
    
    client_id = str(uuid4())
    response = client.get(f'/orders/{client_id}', headers=auth_headers)
    
    assert response.status_code == 200
    response_json = response.get_json()
    assert isinstance(response_json, list)
    assert len(response_json) == 1

@patch('orders_management.src.queries.get_order_by_client.GetOrderByClient.execute')
def test_get_orders_invalid_uuid(mock_execute, client, auth_headers):
    mock_execute.side_effect = InvalidData()
    
    response = client.get('/orders/invalid-uuid', headers=auth_headers)
    assert response.status_code == 400

def test_get_orders_no_token(client):
    client_id = str(uuid4())
    response = client.get(f'/orders/{client_id}')
    assert response.status_code == 401

@patch('orders_management.src.queries.get_order_by_id.GetOrderById.execute')
def test_get_order_by_id_success(mock_execute, client, auth_headers):
    mock_order = {
        'id': str(uuid4()),
        'products': [],
        'client_id': str(uuid4()),
        'date_order': fake.iso8601(),
        'total': fake.pyfloat(left_digits=3, right_digits=2),
        'state': 'pending'
    }
    mock_execute.return_value = mock_order
    
    order_id = str(uuid4())
    response = client.get(f'/orders/order/{order_id}', headers=auth_headers)
    
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['id'] == mock_order['id']

@patch('orders_management.src.queries.get_order_by_id.GetOrderById.execute')
def test_get_order_by_id_not_found(mock_execute, client, auth_headers):
    mock_execute.return_value = None
    
    order_id = str(uuid4())
    response = client.get(f'/orders/order/{order_id}', headers=auth_headers)
    
    assert response.status_code == 404

@patch('orders_management.src.commands.update_orders.UpdateStateOrder.execute')
def test_update_order_status_success(mock_execute, client, auth_headers):
    mock_execute.return_value = {'message': 'Status updated successfully'}
    
    order_id = str(uuid4())
    data = {'state': 'COMPLETED'}
    response = client.put(f'/orders/{order_id}/status',
                         data=json.dumps(data),
                         headers=auth_headers)
    
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['message'] == 'Status updated successfully'

@patch('orders_management.src.commands.update_orders.UpdateStateOrder.execute')
def test_update_order_status_invalid_data(mock_execute, client, auth_headers):
    mock_execute.side_effect = InvalidData()
    
    order_id = str(uuid4())
    data = {'state': 'INVALID_STATE'}
    response = client.put(f'/orders/{order_id}/status',
                         data=json.dumps(data),
                         headers=auth_headers)
    
    assert response.status_code == 400
    response_json = response.get_json()
    assert 'error' in response_json

def test_ping(client):
    response = client.get('/orders/ping')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'pong'}