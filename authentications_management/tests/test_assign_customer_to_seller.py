import unittest
from unittest.mock import MagicMock, patch
from authentications_management.src.commands.assign_customer_to_seller import AssignCustomerToSeller
from authentications_management.src.models.sellers import Sellers
from authentications_management.src.errors.errors import InvalidData, SellerNotFound

class TestAssignCustomerToSeller(unittest.TestCase):

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_success(self, mock_sellers, mock_db_session):
        seller_id = "123e4567-e89b-12d3-a456-426614174000"
        customer_email = "customer1@example.com"
        mock_seller = MagicMock()
        mock_seller.assigned_customers = []

        mock_sellers.query.filter_by.return_value.first.return_value = mock_seller

        data = {"customer_email": customer_email}
        command = AssignCustomerToSeller(data, seller_id)
        response = command.execute()

        mock_sellers.query.filter_by.assert_called_once_with(id=seller_id)
        self.assertIn(customer_email, mock_seller.assigned_customers)
        mock_db_session.commit.assert_called_once()
        self.assertEqual(response, {
            "message": "Customer has been successfully assigned to Seller",
            "seller_id": seller_id,
            "customer_email": customer_email
        })

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_already_exists(self, mock_sellers, mock_db_session):
        seller_id = "123e4567-e89b-12d3-a456-426614174000"
        customer_email = "customer1@example.com"
        mock_seller = MagicMock()
        mock_seller.assigned_customers = [customer_email]

        mock_sellers.query.filter_by.return_value.first.return_value = mock_seller

        data = {"customer_email": customer_email}
        command = AssignCustomerToSeller(data, seller_id)
        response = command.execute()

        mock_sellers.query.filter_by.assert_called_once_with(id=seller_id)
        self.assertEqual(mock_seller.assigned_customers, [customer_email])
        mock_db_session.commit.assert_called_once()
        self.assertEqual(response, {
            "message": "Customer has been successfully assigned to Seller",
            "seller_id": seller_id,
            "customer_email": customer_email
        })

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_missing_customer_email(self, mock_sellers, mock_db_session):
        data = {}
        command = AssignCustomerToSeller(data, "123e4567-e89b-12d3-a456-426614174000")

        with self.assertRaises(InvalidData) as context:
            command.execute()

        self.assertEqual(str(context.exception), "Customer email is required")
        mock_sellers.query.filter_by.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_seller_not_found(self, mock_sellers, mock_db_session):
        mock_sellers.query.filter_by.return_value.first.return_value = None

        data = {"customer_email": "customer1@example.com"}
        command = AssignCustomerToSeller(data, "123e4567-e89b-12d3-a456-426614174000")

        with self.assertRaises(SellerNotFound) as context:
            command.execute()

        self.assertEqual(str(context.exception), "Seller not found")
        mock_sellers.query.filter_by.assert_called_once_with(id="123e4567-e89b-12d3-a456-426614174000")
        mock_db_session.commit.assert_not_called()

    @patch('authentications_management.src.commands.assign_customer_to_seller.db_session')
    @patch('authentications_management.src.commands.assign_customer_to_seller.Sellers')
    def test_assign_customer_database_error(self, mock_sellers, mock_db_session):
        seller_id = "123e4567-e89b-12d3-a456-426614174000"
        customer_email = "customer1@example.com"
        mock_seller = MagicMock()
        mock_seller.assigned_customers = []

        mock_sellers.query.filter_by.return_value.first.return_value = mock_seller
        mock_db_session.commit.side_effect = Exception("Database error")

        data = {"customer_email": customer_email}
        command = AssignCustomerToSeller(data, seller_id)

        with self.assertRaises(RuntimeError) as context:
            command.execute()

        self.assertEqual(str(context.exception), "Database error: Database error")
        mock_db_session.rollback.assert_called_once()