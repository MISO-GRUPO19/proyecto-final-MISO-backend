import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from orders_management.src.commands.generate_seller_visits import GenerateSellerVisits
from orders_management.src.models.visits import Visits, VisitStatus

class TestGenerateSellerVisits(unittest.TestCase):

    @patch("orders_management.src.commands.generate_seller_visits.db_session")
    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    @patch("orders_management.src.commands.generate_seller_visits.requests.post")
    def test_execute_success_creates_visits_when_none_exist(self, mock_post, mock_get, mock_db_session):
        # Mock the token retrieval
        mock_post.return_value.json.return_value = {"access_token": "fake_token"}
        mock_post.return_value.status_code = 200

        # Mock the seller info response
        mock_get.side_effect = [
            MagicMock(
                json=MagicMock(return_value={
                    "assigned_customers": ["customer1@example.com", "customer2@example.com"],
                    "id": "seller-id"
                }),
                status_code=200
            ),
            MagicMock(
                json=MagicMock(return_value=[{
                    "id": "customer1-id",
                    "firstName": "John",
                    "lastName": "Doe",
                    "phoneNumber": "123456789",
                    "address": "123 Main St",
                    "stores": []
                }]),
                status_code=200
            ),
            MagicMock(
                json=MagicMock(return_value=[{
                    "id": "customer2-id",
                    "firstName": "Jane",
                    "lastName": "Smith",
                    "phoneNumber": "987654321",
                    "address": "456 Elm St",
                    "stores": []
                }]),
                status_code=200
            )
        ]

        # Mock the database query to simulate NO existing visits for the month
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_db_session.query.return_value = mock_query

        # Mock add and commit
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        # Execute the command
        command = GenerateSellerVisits(seller_id="seller-id")
        result = command.execute()

        # Assertions
        self.assertEqual(result["seller_id"], "seller-id")
        self.assertEqual(len(result["visits_info"]), 2)
        self.assertEqual(result["visits_info"][0]["customer_name"], "John Doe")
        self.assertEqual(result["visits_info"][1]["customer_name"], "Jane Smith")
        self.assertEqual(result["visits_info"][0]["visit_status"], "NO_VISITADO")
        self.assertEqual(result["visits_info"][1]["visit_status"], "NO_VISITADO")
        self.assertEqual(mock_db_session.add.call_count, 2)
        self.assertEqual(mock_db_session.commit.call_count, 2)

    @patch("orders_management.src.commands.generate_seller_visits.db_session")
    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    @patch("orders_management.src.commands.generate_seller_visits.requests.post")
    def test_execute_skips_if_visit_exists(self, mock_post, mock_get, mock_db_session):
        # Mock the token retrieval
        mock_post.return_value.json.return_value = {"access_token": "fake_token"}
        mock_post.return_value.status_code = 200

        # Mock the seller info response
        mock_get.side_effect = [
            MagicMock(
                json=MagicMock(return_value={
                    "assigned_customers": ["customer1@example.com", "customer2@example.com"],
                    "id": "seller-id"
                }),
                status_code=200
            ),
            MagicMock(
                json=MagicMock(return_value=[{
                    "id": "customer1-id",
                    "firstName": "John",
                    "lastName": "Doe",
                    "phoneNumber": "123456789",
                    "address": "123 Main St",
                    "stores": []
                }]),
                status_code=200
            ),
            MagicMock(
                json=MagicMock(return_value=[{
                    "id": "customer2-id",
                    "firstName": "Jane",
                    "lastName": "Smith",
                    "phoneNumber": "987654321",
                    "address": "456 Elm St",
                    "stores": []
                }]),
                status_code=200
            )
        ]

        # Mock an existing visit for the first customer
        mock_existing_visit = MagicMock(spec=Visits)
        mock_existing_visit.id = "existing-visit-id"
        mock_existing_visit.visit_address = "123 Main St"
        mock_existing_visit.customer_name = "John Doe"
        mock_existing_visit.customer_phonenumber = "123456789"
        mock_existing_visit.store_name = "John Doe Supermercado"
        mock_existing_visit.visit_date = datetime.now() + timedelta(days=1)
        mock_existing_visit.visit_status = VisitStatus.NO_VISITADO

        # Mock the database query to return existing visit for first customer, None for second
        mock_query = MagicMock()
        mock_query.filter.return_value.first.side_effect = [mock_existing_visit, None]
        mock_db_session.query.return_value = mock_query

        # Mock add and commit
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        # Execute the command
        command = GenerateSellerVisits(seller_id="seller-id")
        result = command.execute()

        # Assertions
        self.assertEqual(result["seller_id"], "seller-id")
        self.assertEqual(len(result["visits_info"]), 2)
        self.assertEqual(result["visits_info"][0]["visit_id"], "existing-visit-id")
        self.assertEqual(result["visits_info"][1]["customer_name"], "Jane Smith")
        mock_db_session.add.assert_called_once()  # Only called for the new visit
        mock_db_session.commit.assert_called_once()

    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    def test_get_seller_info_failure(self, mock_get):
        # Mock a failed seller info retrieval
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Seller not found"

        command = GenerateSellerVisits(seller_id="seller-id")
        command.token = "fake_token"
        with self.assertRaises(Exception) as context:
            command.get_seller_info()
        self.assertIn("Seller not found", str(context.exception))

    @patch("orders_management.src.commands.generate_seller_visits.requests.get")
    def test_get_customer_info_failure(self, mock_get):
        # Mock a failed customer info retrieval
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Customer not found"

        command = GenerateSellerVisits(seller_id="seller-id")
        command.token = "fake_token"
        with self.assertRaises(Exception) as context:
            command.get_customer_info("customer@example.com")
        self.assertIn("Customer not found", str(context.exception))