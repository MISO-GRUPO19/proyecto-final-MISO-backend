import unittest
from unittest.mock import patch, MagicMock
from authentications_management.src.queries.get_sellers import GetSellers
from authentications_management.src.models.sellers import Sellers

class TestGetSellers(unittest.TestCase):

    @patch('authentications_management.src.queries.get_sellers.db_session')
    def test_get_sellers_success(self, mock_db_session):
        # Create mock seller objects that match your actual model
        mock_seller_1 = MagicMock(spec=Sellers)
        mock_seller_1.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_seller_1.identification = "123456789"
        mock_seller_1.name = "John Doe"
        mock_seller_1.country = "USA"
        mock_seller_1.address = "123 Main St"
        mock_seller_1.telephone = "555-1234"
        mock_seller_1.email = "john.doe@example.com"
        mock_seller_1.assigned_customers = ["customer1", "customer2"]

        mock_seller_2 = MagicMock(spec=Sellers)
        mock_seller_2.id = "223e4567-e89b-12d3-a456-426614174001"
        mock_seller_2.identification = "987654321"
        mock_seller_2.name = "Jane Smith"
        mock_seller_2.country = "Canada"
        mock_seller_2.address = "456 Elm St"
        mock_seller_2.telephone = "555-5678"
        mock_seller_2.email = "jane.smith@example.com"
        mock_seller_2.assigned_customers = ["customer3"]

        # Mock query result
        mock_db_session.query.return_value.all.return_value = [mock_seller_1, mock_seller_2]

        # Execute query
        get_sellers = GetSellers()
        result = get_sellers.execute()

        # Assertions
        expected_result = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "identification": "123456789",
                "name": "John Doe",
                "country": "USA",
                "address": "123 Main St",
                "telephone": "555-1234",
                "email": "john.doe@example.com",
                "assigned_customers": ["customer1", "customer2"]
            },
            {
                "id": "223e4567-e89b-12d3-a456-426614174001",
                "identification": "987654321",
                "name": "Jane Smith",
                "country": "Canada",
                "address": "456 Elm St",
                "telephone": "555-5678",
                "email": "jane.smith@example.com",
                "assigned_customers": ["customer3"]
            }
        ]
        self.assertEqual(result, expected_result)

    @patch('authentications_management.src.queries.get_sellers.db_session')
    def test_get_sellers_empty(self, mock_db_session):
        # Mock query result
        mock_db_session.query.return_value.all.return_value = []

        # Execute query
        get_sellers = GetSellers()
        result = get_sellers.execute()

        # Assertions
        self.assertEqual(result, [])

    @patch('authentications_management.src.queries.get_sellers.db_session')
    def test_get_sellers_database_error(self, mock_db_session):
        # Mock query to raise an exception
        mock_db_session.query.side_effect = Exception("Database error")

        # Execute query
        get_sellers = GetSellers()

        with self.assertRaises(Exception) as context:
            get_sellers.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Database error")