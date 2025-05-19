import pytest
from unittest.mock import patch, MagicMock
from orders_management.src.commands.create_orders import CreateOrders
from orders_management.src.errors.errors import InvalidData
from flask import Flask
import uuid

@pytest.fixture
def sample_data():
    return {
        "token": "mocked_token",
        "client_id": str(uuid.uuid4()),
        "seller_id": str(uuid.uuid4()),
        "provider_id": str(uuid.uuid4()),
        "route_id": str(uuid.uuid4()),
        "date": "2025-05-01T12:00:00",
        "total": 1500,
        "order_type": "CLIENTE",
        "products": [
            {"barcode": "1234567890", "quantity": 10}
        ]
    }

@patch("orders_management.src.commands.create_orders.requests.get")
@patch("orders_management.src.commands.create_orders.requests.put")
@patch("orders_management.src.commands.create_orders.db_session")
def test_create_order_success(mock_db, mock_put, mock_get, sample_data):
    mock_get.return_value.status_code = 200
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = {}

    order_instance = MagicMock()
    order_instance.id = uuid.uuid4()
    order_instance.state = "PENDIENTE"

    mock_db.add = MagicMock()
    mock_db.flush = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.remove = MagicMock()

    with patch("orders_management.src.commands.create_orders.Orders", return_value=order_instance), \
         patch("orders_management.src.commands.create_orders.OrderStatusHistory"), \
         patch("orders_management.src.commands.create_orders.ProductOrder"):
        command = CreateOrders(**sample_data)
        response, status = command.execute()
        assert status == 201
        assert response.json["message"] == "Sale created successfully"

def test_invalid_data_raises():
    data = {
        "token": "t",
        "client_id": None,  # missing required
        "seller_id": "s",
        "provider_id": "p",
        "route_id": "r",
        "date": "2025-05-01T12:00:00",
        "total": 1500,
        "order_type": "CLIENTE",
        "products": []
    }

    with pytest.raises(InvalidData):
        CreateOrders(**data).execute()

@patch("orders_management.src.commands.create_orders.requests.get")
def test_insufficient_stock_response(mock_get, sample_data):
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"error": "ProductInsufficientStock"}

    command = CreateOrders(**sample_data)
    response, status = command.execute()

    assert status == 400
    assert response.json["error"] == "ProductInsufficientStock"

@patch("orders_management.src.commands.create_orders.requests.get")
def test_product_not_found_response(mock_get, sample_data):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "ProductNotFound"}

    command = CreateOrders(**sample_data)
    response, status = command.execute()

    assert status == 404
    assert response.json["error"] == "ProductNotFound"

