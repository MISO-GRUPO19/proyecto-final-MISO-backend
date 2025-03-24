import unittest
from unittest.mock import patch, MagicMock
from products_management.src.commands.create_massive_products import CreateMassiveProducts
from products_management.src.errors.errors import NotFile
from products_management.src.models.products import Products, Batch
from products_management.src.models.database import db_session
import pandas as pd
import uuid

class TestCreateMassiveProducts(unittest.TestCase):

    @patch('products_management.src.commands.create_massive_products.db_session')
    @patch('pandas.read_excel')
    def test_execute_success(self, mock_read_excel, mock_db_session):
        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        mock_df = pd.DataFrame({
            'name': ['Product1', 'Product2'],
            'description': ['Description1', 'Description2'],
            'price': [10.0, 20.0],
            'category': ['Category1', 'Category2'],
            'weight': [1.0, 2.0],
            'barcode': ['1234567890123', '1234567890124'],
            'provider_id': [str(uuid.uuid4()), str(uuid.uuid4())],
            'batch': ['Batch001', 'Batch002'],
            'best_before': [pd.Timestamp('2025-12-31'), pd.Timestamp('2025-10-31')],
            'quantity': [100, 200]
        })
        mock_read_excel.return_value = mock_df

        command = CreateMassiveProducts(mock_file)

        result = command.execute()

        self.assertEqual(result['message'], 'Productos creados correctamente')
        self.assertTrue(mock_db_session.add_all.called)
        self.assertTrue(mock_db_session.commit.called)

    @patch('products_management.src.commands.create_massive_products.db_session')
    def test_execute_no_file(self, mock_db_session):
        mock_file = MagicMock()
        mock_file.filename = ''

        command = CreateMassiveProducts(mock_file)

        with self.assertRaises(NotFile):
            command.execute()
