import unittest
from unittest.mock import patch, MagicMock
from authentications_management.src.queries.get_seller_by_identification import GetSellerByIdentification
from authentications_management.src.models.sellers import Sellers
from authentications_management.src.errors.errors import SellerNotFound

class TestGetSellerByIdentification(unittest.TestCase):

    @patch("authentications_management.src.queries.get_seller_by_identification.db_session")
    def test_execute_with_valid_identification(self, mock_db_session):
        # Mock the seller object
        mock_seller = MagicMock()
        mock_seller.id = "90cf05da-e547-49eb-8b25-d28b36ebd7f2"
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_seller

        # Execute the query
        query = GetSellerByIdentification("123456789")
        result = query.execute()

        # Assertions
        self.assertEqual(result["seller_id"], "90cf05da-e547-49eb-8b25-d28b36ebd7f2")
        mock_db_session.query.assert_called_once()

    @patch("authentications_management.src.queries.get_seller_by_identification.db_session")
    def test_execute_with_valid_name(self, mock_db_session):
        # Mock the seller object
        mock_seller = MagicMock()
        mock_seller.id = "4e18782e-8a4f-4770-9c27-50fcc3187409"
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_seller

        # Execute the query
        query = GetSellerByIdentification("John Doe")
        result = query.execute()

        # Assertions
        self.assertEqual(result["seller_id"], "4e18782e-8a4f-4770-9c27-50fcc3187409")
        mock_db_session.query.assert_called_once()

    @patch("authentications_management.src.queries.get_seller_by_identification.db_session")
    def test_execute_with_invalid_identification(self, mock_db_session):
        # Mock no seller found
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        # Execute the query and expect an exception
        query = GetSellerByIdentification("invalid_id")
        with self.assertRaises(SellerNotFound):
            query.execute()

        # Assertions
        mock_db_session.query.assert_called_once()
