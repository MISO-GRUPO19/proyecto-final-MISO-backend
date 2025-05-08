import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from orders_management.src.commands.generate_seller_visits import GenerateSellerVisits
from orders_management.src.models.visits import Visits

class TestGenerateSellerVisits(unittest.TestCase):

    @patch("orders_management.src.commands.generate_seller_visits.db_session")
    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    @patch("orders_management.src.commands.generate_seller_visits.requests.post")
    def test_execute_success(self, mock_post, mock_get, mock_db_session):
        # Mock the token retrieval
        mock_post.return_value.json.return_value = {"access_token": "fake_token"}
        mock_post.return_value.status_code = 200

        # Mock the seller info response
        mock_get.side_effect = [
            MagicMock(
                json=MagicMock(return_value={
                    "assigned_customers": ["customer1@example.com", "customer2@example.com"]
                }),
                status_code=200
            ),
            MagicMock(
                json=MagicMock(return_value=[
                    {
                        "id": "customer1-id",
                        "firstName": "John",
                        "lastName": "Doe",
                        "phoneNumber": "123456789",
                        "address": "123 Main St",
                        "stores": []
                    }
                ]),
                status_code=200
            ),
            MagicMock(
                json=MagicMock(return_value=[
                    {
                        "id": "customer2-id",
                        "firstName": "Jane",
                        "lastName": "Smith",
                        "phoneNumber": "987654321",
                        "address": "456 Elm St",
                        "stores": []
                    }
                ]),
                status_code=200
            )
        ]

        # Mock the database session
        mock_db_session.return_value.__enter__.return_value = mock_db_session
        mock_db_session.return_value.__exit__.return_value = None

        # Execute the command
        command = GenerateSellerVisits(seller_id="seller-id")
        result = command.execute()

        # Assertions
        self.assertEqual(result["seller_id"], "seller-id")
        self.assertEqual(len(result["visits_info"]), 2)
        self.assertEqual(result["visits_info"][0]["customer_name"], "John Doe")
        self.assertEqual(result["visits_info"][1]["customer_name"], "Jane Smith")

    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    def test_get_seller_info_failure(self, mock_get):
        # Mock a failed seller info retrieval
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Seller not found"

        # Execute the command
        command = GenerateSellerVisits(seller_id="seller-id")
        command.token = "fake_token"
        with self.assertRaises(Exception) as context:
            command.get_seller_info()

        # Assertions
        self.assertIn("Seller not found", str(context.exception))

    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    def test_get_customer_info_failure(self, mock_get):
        # Mock a failed customer info retrieval
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Customer not found"

        # Execute the command
        command = GenerateSellerVisits(seller_id="seller-id")
        command.token = "fake_token"
        with self.assertRaises(Exception) as context:
            command.get_customer_info("customer@example.com")

        # Assertions
        self.assertIn("Customer not found", str(context.exception))

