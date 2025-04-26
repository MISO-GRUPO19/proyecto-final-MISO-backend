import unittest
from unittest.mock import patch
from types import SimpleNamespace
from products_management.src.queries.get_products import GetProducts  # ajusta si es necesario

class TestGetProducts(unittest.TestCase):

    @patch('products_management.src.queries.get_products.db_session')
    def test_execute_returns_correct_products(self, mock_db_session):
        mock_db_session.query().outerjoin().group_by().all.return_value = [
            SimpleNamespace(name="Producto A", barcode="123ABC", stock=10, price=5.5, category="Electronics"),
            SimpleNamespace(name="Producto B", barcode="456DEF", stock=0, price=7.25, category="Groceries"),
        ]

        service = GetProducts(token="dummy-token")
        result = service.execute()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], "Producto A")
        self.assertEqual(result[0]['barcode'], "123ABC")
        self.assertEqual(result[0]['stock'], 10)
        self.assertEqual(result[0]['price'], 5.5)

    @patch('products_management.src.queries.get_products.db_session')
    def test_execute_handles_exception(self, mock_db_session):
        mock_db_session.query.side_effect = Exception("DB error")

        service = GetProducts(token="dummy-token")
        result = service.execute()

        self.assertIn("error", result)
        self.assertEqual(result['error'], "DB error")