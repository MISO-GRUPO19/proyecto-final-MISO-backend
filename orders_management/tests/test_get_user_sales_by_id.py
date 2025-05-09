'''
import unittest
from unittest.mock import patch, MagicMock
from authentications_management.src.queries.get_seller_sales_by_id import GetSellerSalesById
from authentications_management.src.models.sellers import Sellers, Goals, GoalProduct
from authentications_management.src.errors.errors import SellerNotFound, GoalNotFound
import uuid
import random
from datetime import datetime
class TestGetSellerSalesById(unittest.TestCase):

    @patch('authentications_management.src.queries.get_seller_sales_by_id.db_session')
    def test_seller_not_found(self, mock_db_session):
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(SellerNotFound):
            GetSellerSalesById("nonexistent_seller").execute()

    @patch('authentications_management.src.queries.get_seller_sales_by_id.db_session')
    def test_successful_execution(self, mock_db_session):
        
        mock_seller = Sellers(name="John Doe", identification="123456", country="USA", address="123 Main St", telephone="555-1234", email="john@example.com")
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_seller

        
        mock_goal = Goals(seller_id=mock_seller.id, date=datetime(2025,3,1))
        mock_db_session.query.return_value.filter.return_value.all.side_effect = [
            [mock_goal],  
            [  
                GoalProduct(goal_id=mock_goal.id, sales=1000, sales_expectation=1200, date=mock_goal.date, product_id=uuid.uuid4, quantity=random.randint(1,100)),
                GoalProduct(goal_id=mock_goal.id, sales=800, sales_expectation=1000, date=mock_goal.date, product_id=uuid.uuid4, quantity=random.randint(1,100))
            ]
        ]

        
        result, status_code = GetSellerSalesById("123456").execute()

        self.assertEqual(status_code, 200)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["country"], "USA")
        self.assertEqual(result["total_sales"], 1800)
        self.assertEqual(len(result["monthly_summary"]), 1)
        self.assertEqual(result["monthly_summary"][0]["date"], "03-2025")
        self.assertEqual(result["monthly_summary"][0]["total_sales"], 1800)
        self.assertEqual(result["monthly_summary"][0]["goals"], 2200)
        self.assertAlmostEqual(result["monthly_summary"][0]["goals_achieved"], 81.82, places=2)
'''