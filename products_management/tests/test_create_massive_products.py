import unittest
from unittest.mock import patch, MagicMock
from products_management.src.commands.create_massive_products import CreateMassiveProducts
from products_management.src.errors.errors import NotFile, InvalidFileFormat, ValidationError
from products_management.src.models.products import Products, Batch, Category, Provider
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

        mock_db_session.query.return_value.filter_by.return_value.first.side_effect = [
            MagicMock(spec=Category), MagicMock(spec=Category),
            MagicMock(spec=Provider), MagicMock(spec=Provider)
        ]

        command = CreateMassiveProducts(mock_file)
        result = command.execute()

        self.assertIn('productos cargados correctamente', result['message'].lower())
        self.assertTrue(mock_db_session.add_all.called)
        self.assertTrue(mock_db_session.commit.called)

    @patch('products_management.src.commands.create_massive_products.db_session')
    def test_execute_no_file(self, mock_db_session):
        mock_file = MagicMock()
        mock_file.filename = ''

        command = CreateMassiveProducts(mock_file)

        with self.assertRaises(NotFile):
            command.execute()

    @patch('pandas.read_excel')
    def test_execute_invalid_format(self, mock_read_excel):
        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        mock_df = pd.DataFrame({
            'name': ['Product1'], 'description': ['Description1']  # Falta el resto de columnas requeridas
        })
        mock_read_excel.return_value = mock_df

        command = CreateMassiveProducts(mock_file)

        with self.assertRaises(InvalidFileFormat):
            command.execute()

    @patch('products_management.src.commands.create_massive_products.db_session')
    @patch('pandas.read_excel')
    def test_execute_with_invalid_data(self, mock_read_excel, mock_db_session):
        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        mock_df = pd.DataFrame({
            'name': ['', 'Valid Product'],  # Nombre inválido en la primera fila
            'description': ['Description1', 'Description2'],
            'price': ['Invalid', 20.0],  # Precio inválido en la primera fila
            'category': ['InvalidCategory', 'Category2'],  # Categoría inexistente
            'weight': [1.0, 2.0],
            'barcode': ['1234567890123', '1234567890124'],
            'provider_id': [str(uuid.uuid4()), str(uuid.uuid4())],
            'batch': ['Batch001', 'Batch002'],
            'best_before': [pd.Timestamp('2025-12-31'), pd.Timestamp('2025-10-31')],
            'quantity': [100, 200]
        })
        mock_read_excel.return_value = mock_df
        mock_db_session.query.return_value.filter_by.return_value.first.side_effect = [None, MagicMock(spec=Category), None, MagicMock(spec=Provider)]

        command = CreateMassiveProducts(mock_file)
        result = command.execute()

        self.assertIn('errores en la carga', result['message'].lower())
        self.assertIn('nombre del producto inválido', result['detalles'][0]['errores'][0].lower())
