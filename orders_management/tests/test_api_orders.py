import json
import pytest
from faker import Faker
from unittest.mock import patch, MagicMock
from flask_jwt_extended import create_access_token
from orders_management.src.main import app
from uuid import UUID, uuid4

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

@patch('requests.get')
@patch('src.commands.create_orders.CreateOrders.execute')
def test_create_sale_success(mock_execute, mock_requests_get, client, auth_headers):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"stock_available": True}
    mock_requests_get.return_value = mock_response

    mock_execute.return_value = {'message': 'Order created'}

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


@patch('src.commands.create_orders.CreateOrders.execute')
def test_create_sale_missing_fields(mock_execute, client, auth_headers):
    mock_execute.return_value = {'message': 'Order created with defaults'}

    data = {
        "client_id": str(uuid4()),
        "products": []
    }

    response = client.post('/orders', data=json.dumps(data), headers=auth_headers)
    assert response.status_code == 400

@patch('src.commands.create_orders.CreateOrders.execute')
def test_create_sale_no_token(mock_execute, client):
    data = {
        "client_id": str(uuid4()),
        "products": []
    }

    response = client.post('/orders', data=json.dumps(data))
    assert response.status_code == 401

@patch('src.queries.get_order_by_client.GetOrderByClient.execute')
def test_get_orders_success(mock_execute, client, auth_headers):
    mock_execute.return_value = [{
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
    }]
    
    client_id = str(uuid4())
    client_id = UUID(client_id)

    response = client.get(f'/orders/{client_id}', headers=auth_headers)
    
    assert response.status_code == 200
    response_json = response.get_json()

def test_get_orders_no_token(client):
    client_id = str(uuid4())
    response = client.get(f'/orders/{client_id}')
    assert response.status_code == 401

def test_ping(client):
    response = client.get('/orders/ping')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'pong'}
