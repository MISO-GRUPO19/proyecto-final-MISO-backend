import unittest
from unittest.mock import MagicMock, patch
from authentications_management.src.commands.assign_customer_to_seller import AssignCustomerToSeller
from authentications_management.src.models.sellers import Sellers
from authentications_management.src.errors.errors import InvalidData, SellerNotFound

class TestAssignCustomerToSeller(unittest.TestCase):

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_success(self, mock_sellers, mock_db_session):
        # Mock data
        seller_id = "123e4567-e89b-12d3-a456-426614174000"
        customer_id = "customer_1"
        mock_seller = MagicMock()
        mock_seller.assigned_customers = []

        # Mock seller query
        mock_sellers.query.filter_by.return_value.first.return_value = mock_seller

        # Execute command
        data = {"customer_id": customer_id}
        command = AssignCustomerToSeller(data, seller_id)
        response = command.execute()

        # Assertions
        mock_sellers.query.filter_by.assert_called_once_with(id=seller_id)
        self.assertIn(customer_id, mock_seller.assigned_customers)
        mock_db_session.commit.assert_called_once()
        self.assertEqual(response, {
            "message": "Customer has been successfully assigned to Seller",
            "seller_id": seller_id,
            "customer_id": customer_id
        })

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_already_exists(self, mock_sellers, mock_db_session):
        # Mock data
        seller_id = "123e4567-e89b-12d3-a456-426614174000"
        customer_id = "customer_1"
        mock_seller = MagicMock()
        mock_seller.assigned_customers = [customer_id]

        # Mock seller query
        mock_sellers.query.filter_by.return_value.first.return_value = mock_seller

        # Execute command
        data = {"customer_id": customer_id}
        command = AssignCustomerToSeller(data, seller_id)
        response = command.execute()

        # Assertions
        mock_sellers.query.filter_by.assert_called_once_with(id=seller_id)
        self.assertEqual(mock_seller.assigned_customers, [customer_id])  # No duplicates
        mock_db_session.commit.assert_called_once()
        self.assertEqual(response, {
            "message": "Customer has been successfully assigned to Seller",
            "seller_id": seller_id,
            "customer_id": customer_id
        })

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_missing_customer_id(self, mock_sellers, mock_db_session):
        # Execute command with missing customer_id
        data = {}
        command = AssignCustomerToSeller(data, "123e4567-e89b-12d3-a456-426614174000")

        with self.assertRaises(InvalidData) as context:
            command.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Customer ID is required")
        mock_sellers.query.filter_by.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_seller_not_found(self, mock_sellers, mock_db_session):
        # Mock seller query to return None
        mock_sellers.query.filter_by.return_value.first.return_value = None

        # Execute command
        data = {"customer_id": "customer_1"}
        command = AssignCustomerToSeller(data, "123e4567-e89b-12d3-a456-426614174000")

        with self.assertRaises(SellerNotFound) as context:
            command.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Seller not found")
        mock_sellers.query.filter_by.assert_called_once_with(id="123e4567-e89b-12d3-a456-426614174000")
        mock_db_session.commit.assert_not_called()

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')