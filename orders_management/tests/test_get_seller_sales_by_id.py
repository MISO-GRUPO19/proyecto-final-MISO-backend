import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from orders_management.src.queries.get_seller_sales_by_id import GetSellerSalesById
from orders_management.src.errors.errors import GoalNotFound

class TestGetSellerSalesById(unittest.TestCase):

    @patch.dict("os.environ", {"AUTH": "http://mock-auth-service"})
    @patch("orders_management.src.queries.get_seller_sales_by_id.db_session")
    @patch("orders_management.src.queries.get_seller_sales_by_id.requests.post")
    @patch("orders_management.src.queries.get_seller_sales_by_id.requests.get")
    def test_execute_with_valid_data(self, mock_get, mock_post, mock_db_session):
        # Mock the token retrieval
        mock_post.return_value.json.return_value = {"access_token": "mock_token"}

        # Mock the seller info retrieval
        mock_get.side_effect = [
            MagicMock(json=MagicMock(return_value={
                "id": "90cf05da-e547-49eb-8b25-d28b36ebd7f2",
                "name": "John Doe",
                "country": "USA",
                "phone": "123456789",
                "email": "john.doe@example.com"
            })),
            MagicMock(json=MagicMock(return_value={
                "product_info": {"product_price": 10.0}
            }))
        ]

        # Mock the goals query
        mock_goal = SimpleNamespace(
            id="goal-id-1",
            sales_expectation=1000
        )
        mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_goal]

        # Mock the GoalProduct query
        mock_goal_product = MagicMock()
        mock_goal_product.product_barcode = "1234567890"
        mock_goal_product.date = MagicMock()
        mock_goal_product.date.strftime.return_value = "05-2025"
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_goal_product

        # Mock the total quantity retrieval
        mock_db_session.query.return_value.filter.return_value.scalar.return_value = 50

        # Execute the query
        query = GetSellerSalesById("123456789")
        result, status_code = query.execute()

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["total_sales"], 500.0)
        self.assertEqual(result["monthly_summary"][0]["goals_achieved"], 50.0)

    @patch.dict("os.environ", {"AUTH": "http://mock-auth-service"})
    @patch("orders_management.src.queries.get_seller_sales_by_id.db_session")
    def test_execute_with_no_goals(self, mock_db_session):
        # Mock no goals found
        mock_db_session.query.return_value.filter.return_value.all.return_value = []

        # Execute the query and expect GoalNotFound
        query = GetSellerSalesById("123456789")
        with self.assertRaises(GoalNotFound):
            query.execute()

    @patch.dict("os.environ", {"AUTH": "http://mock-auth-service"})
    @patch("orders_management.src.queries.get_seller_sales_by_id.db_session")
    def test_get_total_quantity_by_barcode(self, mock_db_session):
        # Mock the total quantity retrieval
        mock_db_session.query.return_value.filter.return_value.scalar.return_value = 100

        # Call the method
        query = GetSellerSalesById("123456789")
        total_quantity = query.get_total_quantity_by_barcode(
            seller_id="90cf05da-e547-49eb-8b25-d28b36ebd7f2",
            month=5,
            year=2025,
            product_barcode="1234567890"
        )

        # Assertions
        self.assertEqual(total_quantity, 100)
