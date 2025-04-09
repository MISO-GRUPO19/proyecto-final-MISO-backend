import unittest
from unittest.mock import patch, MagicMock
from manufacturers_management.src.queries.get_manufacturers import GetManufacturer, GetManufacturerById
from manufacturers_management.src.errors.errors import NotExistingManufacturer

class TestGetManufacturer(unittest.TestCase):

    @patch('manufacturers_management.src.queries.get_manufacturers.db_session')
    def test_get_manufacturer_success(self, mock_db_session):
        # Simular un fabricante existente
        mock_session = MagicMock()
        mock_db_session.return_value.__enter__.return_value = mock_session
        mock_manufacturer = MagicMock()
        mock_manufacturer.name = "Test Manufacturer"
        mock_manufacturer.country = "USA"
        mock_manufacturer.contact = "John Doe"
        mock_manufacturer.telephone = "123456789"
        mock_manufacturer.email = "test@example.com"
        mock_manufacturer.id = "valid_uuid"
        mock_session.query.return_value.filter.return_value.first.return_value = mock_manufacturer

        query = GetManufacturer("Test Manufacturer")
        response, status_code = query.execute()

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, {
            "name": "Test Manufacturer",
            "country": "USA",
            "contact": "John Doe",
            "telephone": "123456789",
            "email": "test@example.com",
            "id": "valid_uuid"
        })

    @patch('manufacturers_management.src.queries.get_manufacturers.db_session')
    def test_get_manufacturer_not_existing(self, mock_db_session):
        # Simular un fabricante no existente
        mock_session = MagicMock()
        mock_db_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        query = GetManufacturer("Nonexistent Manufacturer")
        with self.assertRaises(NotExistingManufacturer):
            query.execute()


class TestGetManufacturerById(unittest.TestCase):

    @patch('manufacturers_management.src.queries.get_manufacturers.db_session')
    def test_get_manufacturer_by_id_success(self, mock_db_session):
        # Simular un fabricante existente
        mock_session = MagicMock()
        mock_db_session.return_value.__enter__.return_value = mock_session
        mock_manufacturer = MagicMock()
        mock_manufacturer.name = "Test Manufacturer"
        mock_manufacturer.country = "USA"
        mock_manufacturer.contact = "John Doe"
        mock_manufacturer.telephone = "123456789"
        mock_manufacturer.email = "test@example.com"
        mock_session.query.return_value.filter.return_value.first.return_value = mock_manufacturer

        query = GetManufacturerById(1)
        response, status_code = query.execute()

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, {
            "name": "Test Manufacturer",
            "country": "USA",
            "contact": "John Doe",
            "telephone": "123456789",
            "email": "test@example.com"
        })

    @patch('manufacturers_management.src.queries.get_manufacturers.db_session')
    def test_get_manufacturer_by_id_not_existing(self, mock_db_session):
        # Simular un fabricante no existente
        mock_session = MagicMock()
        mock_db_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        query = GetManufacturerById(999)
        with self.assertRaises(NotExistingManufacturer):
            query.execute()