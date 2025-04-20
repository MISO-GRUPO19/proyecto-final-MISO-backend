import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from datetime import datetime
from orders_management.src.queries.get_order_by_client import GetOrderByClient

# Mock de enumeraciones
class FakeOrderType:
    value = 'CLIENTE'

class FakeState:
    value = 'PENDIENTE'

@pytest.fixture
def mock_order():
    order = MagicMock()
    client_id = uuid4()
    order.id = uuid4()
    order.code = "ORCLABC12345"
    order.client_id = client_id  # UUID
    order.client_id_str = str(client_id)  # Para usar en el test
    order.seller_id = uuid4()
    order.date_order = datetime(2024, 4, 1, 10, 0)
    order.provider_id = uuid4()
    order.total = 200
    order.type = FakeOrderType()
    order.state = FakeState()
    order.route_id = uuid4()

    # Mock de productos en el pedido
    product_item = MagicMock()
    product_item.product_barcode = "ABC123"
    product_item.quantity = 5
    order.product_items = [product_item]

    # Mock de historial de estados
    status = MagicMock()
    status.state = FakeState()
    status.timestamp = datetime(2024, 4, 1, 12, 0)
    order.status_history = [status]

    return order

@patch("orders_management.src.queries.get_order_by_client.db_session")
@patch.object(GetOrderByClient, "_get_product_info")
@patch.object(GetOrderByClient, "_get_seller_info")
def test_execute_success(mock_get_seller_info, mock_get_product_info, mock_db_session, mock_order):
    # 1. Simular retorno de la base de datos
    mock_db_session.query.return_value.filter.return_value.options.return_value.all.return_value = [mock_order]

    # 2. Simular info de producto
    mock_get_product_info.return_value = {"product_name": "Producto Prueba"}

    # 3. Simular info de vendedor
    mock_get_seller_info.return_value = {
        "name": "Ana Gómez",
        "identification": "999888777",
        "country": "CO",
        "address": "Calle Falsa 123",
        "telephone": "3001234567",
        "email": "ana@example.com"
    }

    token = "mock-token"
    query = GetOrderByClient(token, mock_order.client_id_str)
    result = query.execute()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["client_id"] == mock_order.client_id_str
    assert result[0]["products"][0]["name"] == "Producto Prueba"
    assert result[0]["seller_info"]["name"] == "Ana Gómez"
    assert result[0]["state"] == "PENDIENTE"


@patch("orders_management.src.queries.get_order_by_client.db_session")
def test_execute_error(mock_db_session):
    # Simular error en consulta
    mock_db_session.query.side_effect = Exception("DB Falla")

    token = "mock-token"
    client_id = str(uuid4())

    query = GetOrderByClient(token, client_id)
    result = query.execute()

    assert isinstance(result, list)
    assert len(result) == 1
    assert "error" in result[0]
    assert result[0]["error"] == "Failed to retrieve orders"
