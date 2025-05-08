import unittest
from unittest.mock import patch, MagicMock
from customers_management.src.queries.get_customer_by_email import GetCustomerByEmail
from customers_management.src.models.customers import Customers
from customers_management.src.errors.errors import CustomerNotFound

class TestGetCustomerByEmail(unittest.TestCase):

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_success(self, mock_db_session):
        # Mock data
        mock_customer = Customers(
            id="123e4567-e89b-12d3-a456-426614174000",
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            phoneNumber="555-1234",
            address="123 Main St",
            country="USA",
            seller_assigned="seller_1"
        )

        # Mock query result
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_customer

        # Execute query
        get_customer = GetCustomerByEmail("john.doe@example.com")
        result = get_customer.execute()

        # Assertions
        expected_result = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phoneNumber": "555-1234",
            "address": "123 Main St",
            "country": "USA",
            "seller_assigned": "seller_1"
        }
        self.assertEqual(result, expected_result)

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_not_found(self, mock_db_session):
        # Mock query result to return None
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        # Execute query
        get_customer = GetCustomerByEmail("nonexistent@example.com")

        with self.assertRaises(CustomerNotFound) as context:
            get_customer.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Customer with email nonexistent@example.com not found")

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_database_error(self, mock_db_session):
        # Mock query to raise an exception
        mock_db_session.query.side_effect = Exception("Database error")

        # Execute query
        get_customer = GetCustomerByEmail("john.doe@example.com")

        with self.assertRaises(Exception) as context:
            get_customer.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Error fetching customer: Database error")