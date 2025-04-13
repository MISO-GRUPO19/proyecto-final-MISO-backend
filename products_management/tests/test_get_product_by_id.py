import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from products_management.src.queries.get_product_by_id import GetById
from products_management.src.errors.errors import NotFound

class TestGetById(unittest.TestCase):

    @patch('products_management.src.queries.get_product_by_id.requests.get')
    @patch('products_management.src.queries.get_product_by_id.ProductWarehouse.query')
    @patch('products_management.src.queries.get_product_by_id.Products.query')
    def test_execute_returns_correct_data(self, mock_products_query, mock_product_warehouse_query, mock_requests_get):
        
        mock_products_query.filter.return_value.first.return_value = SimpleNamespace(
            name="Producto A",
            weight=1.5,
            provider_id="provider-id-1",
            price=19.99,
            category="Lácteos y Huevos",
            barcode="123ABC"
        )

        mock_product_warehouse_query.filter.return_value.all.return_value = [
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

        mock_requests_get.return_value.json.return_value = {"name": "Proveedor A"}

        service = GetById(identificator="123ABC", token="dummy-token")
        response, status_code = service.execute()

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json["product_info"]["product_name"], "Producto A")
        self.assertEqual(response.json["product_info"]["product_provider_name"], "Proveedor A")
        self.assertEqual(len(response.json["warehouse_info"]), 2)
        self.assertEqual(response.json["warehouse_info"][0]["warehouse_name"], "Bodega A")
        self.assertEqual(response.json["warehouse_info"][1]["warehouse_name"], "Bodega B")

    @patch('products_management.src.queries.get_product_by_id.Products.query')
    def test_execute_raises_not_found(self, mock_products_query):

        mock_products_query.filter.return_value.first.return_value = None
        service = GetById(identificator="123ABC", token="dummy-token")
        response = service.execute()

        self.assertEqual(response.json["error"], "El producto no existe")