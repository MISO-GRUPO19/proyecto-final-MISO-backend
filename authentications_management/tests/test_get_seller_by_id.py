import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from authentications_management.src.queries.get_seller_by_id import GetSellersById
from authentications_management.src.models.sellers import Sellers


class TestGetSellersById(unittest.TestCase):
    def setUp(self):
        self.fake_id = uuid4()
        self.fake_seller = Sellers(
            id=self.fake_id,
            name="John Doe",
            identification="ID123456",
            country="USA",
            address="123 Main Street",
            telephone="+1-555-1234",
            email="john.doe@example.com",
            assigned_customers=["customer1@example.com", "customer2@example.com"]
        )

    @patch("app.endpoints.get_seller_by_id.db_session")
    def test_execute_returns_seller_data(self, mock_db_session):
        mock_session = MagicMock()
        mock_query = mock_session.return_value.query.return_value
        mock_query.filter.return_value.first.return_value = self.fake_seller

        # Setup session context manager
        mock_db_session.return_value = mock_session
        mock_session.__enter__.return_value = mock_session
        mock_session.__exit__.return_value = None

        get_seller = GetSellersById(str(self.fake_id))
        result = get_seller.execute()

        expected = {
            "id": str(self.fake_id),
            "name": "John Doe",
            "identification": "ID123456",
            "country": "USA",
            "address": "123 Main Street",
            "telephone": "+1-555-1234",
            "email": "john.doe@example.com",
            "assigned_customers": [
                "customer1@example.com",
                "customer2@example.com"
            ]
        }

        self.assertEqual(result, expected)

    @patch("app.endpoints.get_seller_by_id.db_session")
    def test_execute_seller_not_found(self, mock_db_session):
        mock_session = MagicMock()
        mock_query = mock_session.return_value.query.return_value
        mock_query.filter.return_value.first.return_value = None

        mock_db_session.return_value = mock_session
        mock_session.__enter__.return_value = mock_session
        mock_session.__exit__.return_value = None

        get_seller = GetSellersById(str(self.fake_id))
        result = get_seller.execute()

        self.assertEqual(result, ({"error": "Seller not found"}, 404))

    def test_invalid_seller_id_format(self):
        with self.assertRaises(ValueError) as context:
            GetSellersById("not-a-valid-uuid")
        self.assertEqual(str(context.exception), "Invalid seller ID format")