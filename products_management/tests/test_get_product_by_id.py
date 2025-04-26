import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from products_management.src.queries.get_product_by_id import GetById
from products_management.src.errors.errors import NotFound

class TestGetById(unittest.TestCase):

    @patch('products_management.src.queries.get_product_by_id.requests.get')
    @patch('products_management.src.queries.get_product_by_id.db_session')
    def test_execute_returns_correct_data(self, mock_db_session, mock_requests_get):
        # Crea un mock de sesión con los queries simulados
        mock_session = MagicMock()
        
        # Producto simulado
        mock_session.query.return_value.filter.return_value.first.return_value = SimpleNamespace(
            name="Producto A",
            weight=1.5,
            provider_id="provider-id-1",
            price=19.99,
            category="Lácteos y Huevos",
            barcode="123ABC"
        )

        # Almacenes simulados
        mock_session.query.return_value.filter.return_value.all.return_value = [
            SimpleNamespace(
                warehouse_name="Bodega A",
                warehouse_address="123 Main St",
                quantity=100,
                shelf="A",
                aisle="1",
                level=1
            ),
            SimpleNamespace(
                warehouse_name="Bodega B",
                warehouse_address="456 Elm St",
                quantity=50,
                shelf="B",
                aisle="2",
                level=2
            )
        ]

        mock_db_session.return_value = mock_session

        # Simula respuesta del proveedor
        mock_requests_get.return_value.json.return_value = {"name": "Proveedor A"}
        mock_requests_get.return_value.raise_for_status = lambda: None  # evita que falle aquí

        service = GetById(identificator="123ABC", token="dummy-token")
        response, status_code = service.execute()

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json["product_info"]["product_name"], "Producto A")
        self.assertEqual(response.json["product_info"]["product_provider_name"], "Proveedor A")
        self.assertEqual(len(response.json["warehouse_info"]), 2)
        self.assertEqual(response.json["warehouse_info"][0]["warehouse_name"], "Bodega A")
        self.assertEqual(response.json["warehouse_info"][1]["warehouse_name"], "Bodega B")
        
    @patch('products_management.src.queries.get_product_by_id.db_session')
    def test_execute_raises_not_found(self, mock_db_session):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_db_session.return_value = mock_session

        service = GetById(identificator="123ABC", token="dummy-token")
        response, status_code = service.execute()

        self.assertEqual(status_code, 404)
        self.assertEqual(response.json["error"], "El producto no existe")