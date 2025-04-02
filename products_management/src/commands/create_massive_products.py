import logging

from dotenv import load_dotenv
import requests
from .base_command import BaseCommand
from ..errors.errors import NotFile, InvalidFileFormat, ERROR_MESSAGES
from ..models.database import db_session
from ..pubsub.publisher import publish_message
import pandas as pd
import os

load_dotenv()

load_dotenv('../.env.development')

NGINX = os.getenv("NGINX")

class CreateMassiveProducts(BaseCommand):
    REQUIRED_COLUMNS = {'name', 'description', 'price', 'category', 'weight', 'barcode', 'provider', 'batch', 'best_before', 'quantity'}
    ALLOWED_CATEGORIES = ["Frutas y Verduras", "Carnes y Pescados", "Lácteos y Huevos", "Panadería y Repostería", "Despensa", "Bebidas", "Snacks y Dulces", "Condimentos y Especias", "Productos de Limpieza", "Productos para Bebés"]
    def __init__(self, file, auth_token):
        self.file = file
        self.auth_token = auth_token
    
    def validate_data(self, df):
        errors = []
        valid_products = []
        
        for index, row in df.iterrows():
            error_messages = []
            
            # Validar nombre
            if not isinstance(row['name'], str) or not row['name'].strip() or len(row['name']) > 100:
                error_messages.append(ERROR_MESSAGES["invalid_product_name"])
            
            # Validar peso, precio y cantidad
            try:
                weight = float(row['weight'])
                price = float(row['price'])
                quantity = int(row['quantity'])
            except ValueError:
                error_messages.append(ERROR_MESSAGES["invalid_weight_price_quantity"])
            
            # Validar categoría
            if row['category'] not in self.ALLOWED_CATEGORIES:
                errors.append(ERROR_MESSAGES["invalid_category"])
            
            # Validar proveedor
            try:
                provider = row['provider']
                headers = {
                    "Authorization": f"Bearer {self.auth_token}"
                }
                response = requests.get(f'{NGINX}/manufacturers?name={provider}', headers=headers)                
                
                if response.status_code != 200:
                    error_messages.append(ERROR_MESSAGES["invalid_provider"])
                else:
                    provider_data = response.json()
                    if 'id' in provider_data:
                        row['provider_id'] = provider_data['id']
                    else:
                        error_messages.append(ERROR_MESSAGES["invalid_provider"])
            except ValueError:
                error_messages.append(ERROR_MESSAGES["invalid_provider"])
            
            if error_messages:
                errors.append({"fila": index + 1, "errores": error_messages})
            else:
                valid_products.append(row)
        
        return valid_products, errors
        
    def execute(self):
        print('Ejecutando comando para carga masiva de productos')
        if self.file.filename == '':
            raise NotFile
        
        try:
            df = pd.read_excel(self.file)
            if not set(df.columns).issuperset(self.REQUIRED_COLUMNS):
                raise InvalidFileFormat(ERROR_MESSAGES["invalid_file_format"])
            
            print(f'Procesando archivo {self.file.filename}')
            valid_products, errors = self.validate_data(df)
            
            print(f'Errores: {errors}')
            if errors:
                return {"message": "Errores en la carga", "detalles": errors}
            
            # Convertir cada fila a un diccionario para que sea serializable
            valid_products_dicts = [row.to_dict() for row in valid_products]
            
            # Convertir Timestamps a cadenas de texto
            for product in valid_products_dicts:
                if isinstance(product['best_before'], pd.Timestamp):
                    product['best_before'] = product['best_before'].strftime('%Y-%m-%d')
            
            # Publicar mensaje en Pub/Sub
            print(f'Cargando {len(valid_products)} productos')
            
            publish_message('products', {'valid_products': valid_products_dicts})
            
            return {'message': f'{len(valid_products)} productos cargados correctamente'}
        
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()