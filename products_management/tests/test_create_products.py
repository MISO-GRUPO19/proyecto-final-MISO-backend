import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from products_management.src.api.products import products
from products_management.src.models.database import db_session
from products_management.src.commands.create_products import CreateProducts
from products_management.src.errors.errors import InvalidData

class TestCreateProducts(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'qwerty'  # Cambia esto por una clave secreta segura
        self.app.config['TESTING'] = True

        jwt = JWTManager(self.app)
        self.app.register_blueprint(products)

        self.client = self.app.test_client()

        with self.app.app_context():
            db_session.remove()

    def tearDown(self):
        with self.app.app_context():
            db_session.remove()

    def get_jwt_token(self):
        with self.app.app_context():
            access_token = create_access_token(identity='test_user')
            return access_token
    @patch('requests.get') 
    def test_create_product(self, mock_requests_get):
        token = self.get_jwt_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with self.client:
            
            # Simular respuesta HTTP para validar proveedores
            mock_requests_get.return_value.status_code = 200
            mock_requests_get.return_value.json.return_value = {"valid": True}
            
            response = self.client.post('/products', json={
                'name': 'Product Name',
                'description': 'Product Description',
                'price': 19.99,
                'category': 'Condimentos y Especias',
                'weight': 1.5,
                'barcode': '1234567890123',
                'provider_id': '123e4567-e89b-12d3-a456-426614174000',
                'batch': 'Batch001',
                'best_before': '2025-12-31T23:59:59',
                'quantity': 100
            }, headers=headers)
            print(response.json)
            self.assertEqual(response.status_code, 201)
            self.assertIn('Producto creado exitosamente', response.json['message'])

    def test_create_product_invalid_name(self):
        data = {
            "name": "@@",  # Nombre inválido
            "description": "Producto válido",
            "price": "20.99",
            "category": "Condimentos y Especias",
            "weight": "1,5",
            "weight_unit": "kg",
            "barcode": "1234567890123",
            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
            "batch": "Batch001",
            "best_before": "2026-12-31T23:59:59",
            "quantity": "100"
        }
        
        auth_token = self.get_jwt_token()  # Obtener el token JWT
        command = CreateProducts(data, auth_token)  # Pasar el token al constructor
                
        with self.assertRaises(InvalidData) as e:
            command.execute()
        
        self.assertIn("El nombre debe tener entre 3 y 100 caracteres", str(e.exception))


    def test_create_product_invalid_category(self):
            data = {
                "name": "Valid Product",
                "description": "Valid description",
                "price": "15.99",
                "category": "InvalidCategory",
                "weight": "2.5",
                "barcode": "1234567890123",
                "provider_id": "123e4567-e89b-12d3-a456-426614174000",
                "batch": "Batch002",
                "best_before": "2025-12-31T23:59:59",
                "quantity": "50"
            }
        
            auth_token = self.get_jwt_token()  # Obtener el token JWT
            command = CreateProducts(data, auth_token)  # Pasar el token al constructor
                    
            with self.assertRaises(InvalidData) as e:
                command.execute()
            
            self.assertIn("Categoría inválida", str(e.exception))

    def test_create_product_invalid_price(self):
        data = {
            "name": "Valid Product",
            "description": "Valid description",
            "price": "abc",  # Precio inválido
            "category": "Condimentos y Especias",
            "weight": "2.5",
            "barcode": "1234567890123",
            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
            "batch": "Batch002",
            "best_before": "2025-12-31T23:59:59",
            "quantity": "50"
        }
    
        auth_token = self.get_jwt_token()  # Obtener el token JWT
        command = CreateProducts(data, auth_token)  # Pasar el token al constructor
                
        with self.assertRaises(InvalidData) as e:
            command.execute()
        
        self.assertIn("Precio inválido", str(e.exception))

    def test_create_product_expired_best_before(self):
        data = {
            "name": "Valid Product",
            "description": "Valid description",
            "price": "19.99",
            "category": "Condimentos y Especias",
            "weight": "1.5",
            "barcode": "1234567890123",
            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
            "batch": "Batch003",
            "best_before": "2000-01-01T00:00:00",  # Fecha expirada
            "quantity": "100"
        }
    
        auth_token = self.get_jwt_token()  # Obtener el token JWT
        command = CreateProducts(data, auth_token)  # Pasar el token al constructor
                
        with self.assertRaises(InvalidData) as e:
            command.execute()
        
        self.assertIn("La fecha de vencimiento debe ser mayor o igual a la fecha actual", str(e.exception))

    def test_create_product_invalid_provider_id(self):
        data = {
            "name": "Valid Product",
            "description": "Valid description",
            "price": "19.99",
            "category": "Condimentos y Especias",
            "weight": "1.5",
            "barcode": "1234567890123",
            "provider_id": "invalid_uuid",  # UUID inválido
            "batch": "Batch004",
            "best_before": "2025-12-31T23:59:59",
            "quantity": "100"
        }
        
        auth_token = self.get_jwt_token()  # Obtener el token JWT
        command = CreateProducts(data, auth_token)  # Pasar el token al constructor
                
        with self.assertRaises(InvalidData) as e:
            command.execute()
        
        self.assertIn("Proveedor inválido", str(e.exception))
    
    @patch('requests.get') 
    def test_create_product_db_failure(self, mock_requests_get):
        data = {
            "name": "Valid Product",
            "description": "Valid description",
            "price": "19.99",
            "category": "Condimentos y Especias",
            "weight": "1.5",
            "barcode": "1234567890123",
            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
            "batch": "Batch005",
            "best_before": "2025-12-31T23:59:59",
            "quantity": "100"
        }
        # Simular respuesta HTTP para validar proveedores
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {"valid": True}
            
        auth_token = self.get_jwt_token()  # Obtener el token JWT
        command = CreateProducts(data, auth_token)  # Pasar el token al constructor
        
        with unittest.mock.patch("products_management.src.models.database.db_session.flush", side_effect=Exception("DB Error")):
            response = command.execute()
            self.assertIn("error", response)
            self.assertIn("Ocurrió un error al guardar el producto", response["error"])
    
    def test_create_product_invalid_weight(self):
        data = {
            "name": "Valid Product",
            "description": "Valid description",
            "price": "19.99",
            "category": "Electronics",
            "weight": "-1",  # Peso inválido
            "barcode": "1234567890123",
            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
            "batch": "Batch006",
            "best_before": "2025-12-31T23:59:59",
            "quantity": "100"
        }
        
        auth_token = self.get_jwt_token()  # Obtener el token JWT
        command = CreateProducts(data, auth_token)  # Pasar el token al constructor
            
        with self.assertRaises(InvalidData) as e:
            command.execute()
        
        self.assertIn("El peso debe ser mayor que cero.", str(e.exception))
    
    def test_create_warehouses(self, mock_requests_get):
        data = {
        "name": "Product Name",
        "description": "Product Description",
        "price": 19.99,
        "category": "Condimentos y Especias",
        "weight": 1.5,
        "barcode": "1234567890123",
        "provider_id": "123e4567-e89b-12d3-a456-426614174000",
        "batch": "Batch001",
        "best_before": "2025-12-31T23:59:59",
        "quantity": 100
        }
    
        auth_token = self.get_jwt_token()  
        command = CreateProducts(data, auth_token)  
        command.execute()  
        with self.app.app_context():
            from products_management.src.models.products import Warehouses
            warehouses = db_session.query(Warehouses).all()  

            self.assertGreater(len(warehouses), 0)

        

    def test_ping(self):
        with self.client:
            response = self.client.get('/products/ping')
            self.assertEqual(response.status_code, 200)
            self.assertIn('pong', response.json['message'])