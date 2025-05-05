import json
import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from uuid import uuid4
from orders_management.src.errors.errors import InvalidData

fake = Faker()

@patch('requests.get')
def test_create_order_invalid_data(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    from orders_management.src.commands.create_orders import CreateOrders
    with pytest.raises(InvalidData):
        CreateOrders(
            token="valid_token",
            client_id=str(uuid4()),
            seller_id=None,
            date=None,
            provider_id=None,
            total=None,
            order_type=None,
            route_id=None,
            products=[]
        ).execute()

@patch('requests.get')
def test_create_order_insufficient_stock(mock_get):
    mock_get.return_value = MagicMock(
        status_code=400,
        json=lambda: {"error": "ProductInsufficientStock"}
    )
    from orders_management.src.commands.create_orders import CreateOrders
    result = CreateOrders(
        token="valid_token",
        client_id=str(uuid4()),
        seller_id=str(uuid4()),
        date="2023-01-01",
        provider_id=str(uuid4()),
        total=100.50,
        order_type="CLIENTE",
        route_id=str(uuid4()),
        products=[{"barcode": "123456789012", "quantity": 2}]
    ).execute()
    assert result[1] == 400
    assert json.loads(result[0].data)['error'] == 'ProductInsufficientStock'

@patch('requests.get')
def test_create_order_product_not_found(mock_get):
    mock_get.return_value = MagicMock(
        status_code=404,
        json=lambda: {"error": "ProductNotFound"}
    )
    from orders_management.src.commands.create_orders import CreateOrders
    result = CreateOrders(
        token="valid_token",
        client_id=str(uuid4()),
        seller_id=str(uuid4()),
        date="2023-01-01",
        provider_id=str(uuid4()),
        total=100.50,
        order_type="CLIENTE",
        route_id=str(uuid4()),
        products=[{"barcode": "123456789012", "quantity": 2}]
    ).execute()
    assert result[1] == 404
    assert json.loads(result[0].data)['error'] == 'ProductNotFound'

@patch('requests.get')
@patch('orders_management.src.models.database.db_session')
def test_create_order_db_error(mock_db, mock_get):
    mock_db.commit.side_effect = Exception("DB error")
    mock_get.return_value = MagicMock(status_code=200)
    from orders_management.src.commands.create_orders import CreateOrders
    with pytest.raises(Exception):
        CreateOrders(
            token="valid_token",
            client_id=str(uuid4()),
            seller_id=str(uuid4()),
            date="2023-01-01",
            provider_id=str(uuid4()),
            total=100.50,
            order_type="CLIENTE",
            route_id=str(uuid4()),
            products=[{"barcode": "123456789012", "quantity": 2}]
        ).execute()

def test_create_order_invalid_date_format():
    from orders_management.src.commands.create_orders import CreateOrders
    with pytest.raises(ValueError):
        CreateOrders(
            token="valid_token",
            client_id=str(uuid4()),
            seller_id=str(uuid4()),
            date="invalid-date",
            provider_id=str(uuid4()),
            total=100.50,
            order_type="CLIENTE",
            route_id=str(uuid4()),
            products=[{"barcode": "123456789012", "quantity": 2}]
        ).execute()

@patch('requests.get')
@patch('requests.put')
def test_create_order_product_update_failure(mock_put, mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    mock_put.return_value = MagicMock(
        status_code=400,
        json=lambda: {"error": "Update failed"}
    )
    from orders_management.src.commands.create_orders import CreateOrders
    result = CreateOrders(
        token="valid_token",
        client_id=str(uuid4()),
        seller_id=str(uuid4()),
        date="2023-01-01",
        provider_id=str(uuid4()),
        total=100.50,
        order_type="CLIENTE",
        route_id=str(uuid4()),
        products=[{"barcode": "123456789012", "quantity": 2}]
    ).execute()
    assert result[1] == 400
    assert 'error' in json.loads(result[0].data)

@patch('requests.get')
def test_create_order_invalid_product_data(mock_get):
    mock_get.return_value = MagicMock(
        status_code=400,
        json=lambda: {"error": "Invalid product data"}
    )
    from orders_management.src.commands.create_orders import CreateOrders
    result = CreateOrders(
        token="valid_token",
        client_id=str(uuid4()),
        seller_id=str(uuid4()),
        date="2023-01-01",
        provider_id=str(uuid4()),
        total=100.50,
        order_type="CLIENTE",
        route_id=str(uuid4()),
        products=[{"barcode": "invalid-barcode", "quantity": 0}]
    ).execute()
    assert result[1] == 400
    assert 'error' in json.loads(result[0].data)

def test_create_order_empty_products():
    from orders_management.src.commands.create_orders import CreateOrders
    with pytest.raises(InvalidData):
        CreateOrders(
            token="valid_token",
            client_id=str(uuid4()),
            seller_id=str(uuid4()),
            date="2023-01-01",
            provider_id=str(uuid4()),
            total=100.50,
            order_type="CLIENTE",
            route_id=str(uuid4()),
            products=[]
        ).execute()