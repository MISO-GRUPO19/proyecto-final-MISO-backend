import unittest
from unittest.mock import patch, MagicMock
from orders_management.src.commands.create_seller_goals import CreateSellerGoals
from orders_management.src.models.goals import Goals, GoalProduct
from orders_management.src.errors.errors import InvalidData

class TestCreateSellerGoals(unittest.TestCase):

    @patch("orders_management.src.commands.create_seller_goals.db_session")
    @patch("orders_management.src.commands.create_seller_goals.requests.post")
    @patch("orders_management.src.commands.create_seller_goals.requests.get")
    def test_execute_with_valid_data(self, mock_get, mock_post, mock_db_session):
        # Mock the token retrieval
        mock_post.return_value.json.return_value = {"access_token": "mock_token"}

        # Mock the product price retrieval
        mock_get.return_value.json.return_value = {
            "product_info": {"product_price": 10.0}
        }

        # Mock the database session
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        # Input data
        data = {
            "seller_id": "90cf05da-e547-49eb-8b25-d28b36ebd7f2",
            "goals": [
                {"product_barcode": "1234567890", "quantity": 5},
                {"product_barcode": "0987654321", "quantity": 10}
            ]
        }

        # Execute the command
        command = CreateSellerGoals(data)
        result = command.execute()

        # Assertions
        self.assertEqual(result["message"], "goals per product have been created successfully")
        self.assertEqual(mock_db_session.add.call_count, 4)  # 2 Goals + 2 GoalProducts
        mock_db_session.commit.assert_called()

    def test_execute_with_missing_required_fields(self):
        # Input data missing "seller_id"
        data = {
            "goals": [
                {"product_barcode": "1234567890", "quantity": 5}
            ]
        }

        # Execute the command and expect an InvalidData exception
        with self.assertRaises(InvalidData) as context:
            command = CreateSellerGoals(data)
            command.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Missing required field: seller_id")

    def test_execute_with_invalid_goals(self):
        # Input data with invalid "goals" field
        data = {
            "seller_id": "90cf05da-e547-49eb-8b25-d28b36ebd7f2",
            "goals": "invalid_goals_field"
        }

        # Execute the command and expect an InvalidData exception
        with self.assertRaises(InvalidData) as context:
            command = CreateSellerGoals(data)
            command.execute()

        # Assertions
        self.assertEqual(str(context.exception), "The goals field must be a non-empty list")

    @patch("orders_management.src.commands.create_seller_goals.requests.get")
    def test_get_product_price(self, mock_get):
        # Mock the product price retrieval
        mock_get.return_value.json.return_value = {
            "product_info": {"product_price": 15.5}
        }

        # Create the command instance
        command = CreateSellerGoals({})
        command.token = "mock_token"  # Mock the token

        # Call the method
        product_price = command.get_product_price("1234567890")

        # Assertions
        self.assertEqual(product_price, 15.5)
        mock_get.assert_called_once()
