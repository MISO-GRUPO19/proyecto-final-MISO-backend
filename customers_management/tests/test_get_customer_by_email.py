import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from flask import jsonify
from customers_management.src.queries.get_customer_by_email import GetCustomerByEmail

class TestGetCustomerByEmail(unittest.TestCase):

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_success(self, mock_db_session):
        # Create mock store objects
        mock_store = MagicMock()
        mock_store.store_name = "Main Store"
        mock_store.address = "123 Business Rd"
        
        # Create mock customer with stores relationship
        mock_customer = MagicMock()
        mock_customer.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_customer.firstName = "John"
        mock_customer.lastName = "Doe"
        mock_customer.email = "john.doe@example.com"
        mock_customer.phoneNumber = "555-1234"
        mock_customer.address = "123 Main St"
        mock_customer.country = "USA"
        
        # Mock the stores relationship
        type(mock_customer).stores = PropertyMock(return_value=[mock_store])

        # Mock the database session
        mock_db_session.return_value.__enter__.return_value.query.return_value\
            .filter.return_value.all.return_value = [mock_customer]

        # Execute query
        get_customer = GetCustomerByEmail("john.doe@example.com")
        response, status_code = get_customer.execute()

        # Assertions
        expected_result = [{
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phoneNumber": "555-1234",
            "address": "123 Main St",
            "country": "USA",
            "stores": [{
                "store_name": "Main Store",
                "store_address": "123 Business Rd"
            }]
        }]
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, expected_result)

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_empty_stores(self, mock_db_session):
        # Create mock customer with empty stores
        mock_customer = MagicMock()
        mock_customer.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_customer.firstName = "John"
        mock_customer.lastName = "Doe"
        mock_customer.email = "john.doe@example.com"
        mock_customer.phoneNumber = "555-1234"
        mock_customer.address = "123 Main St"
        mock_customer.country = "USA"
        type(mock_customer).stores = PropertyMock(return_value=[])

        # Mock the database session
        mock_db_session.return_value.__enter__.return_value.query.return_value\
            .filter.return_value.all.return_value = [mock_customer]

        # Execute query
        get_customer = GetCustomerByEmail("john.doe@example.com")
        response, status_code = get_customer.execute()

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json[0]['stores'], [])

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_not_found(self, mock_db_session):
        # Mock empty result
        mock_db_session.return_value.__enter__.return_value.query.return_value\
            .filter.return_value.all.return_value = []

        # Execute query
        get_customer = GetCustomerByEmail("nonexistent@example.com")
        response, status_code = get_customer.execute()

        # Assertions
        self.assertEqual(status_code, 404)
        self.assertEqual(response.json, {"error": "Customer not found"})

    @patch('customers_management.src.queries.get_customer_by_email.db_session')
    def test_get_customer_by_email_database_error(self, mock_db_session):
        # Mock database error
        mock_db_session.return_value.__enter__.return_value.query.side_effect = Exception("Database error")

        # Execute query
        get_customer = GetCustomerByEmail("john.doe@example.com")

        with self.assertRaises(Exception) as context:
            get_customer.execute()

        # Assertions
        self.assertEqual(str(context.exception), "Database error")