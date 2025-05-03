from dotenv import load_dotenv
import requests
from .base_command import BaseCommand
from ..errors.errors import InvalidData, ERROR_MESSAGES
from ..models.products import Products, ProductWarehouse, Warehouses
from ..models.products import Products
from ..models.batches import Batches
from ..models.database import db_session
import uuid
import re
from datetime import datetime
import os
import random

load_dotenv()

load_dotenv('../.env.development')

MANUFACTURERS = os.getenv("MANUFACTURERS")

class CreateProducts(BaseCommand):
    WAREHOUSE_NAMES = ["Bodega A1", "Bodega A2", "Bodega A3", "Bodega A4", "Bodega A5"]
    WAREHOUSE_ADDRESSES = [
    "Calle 123 #45-67, Bogotá, Colombia",
    "Avenida Siempre Viva 742, Medellín, Colombia",
    "Carrera 10 #20-30, Cali, Colombia",
    "Diagonal 25 #15-50, Barranquilla, Colombia",
    "Transversal 8 #12-34, Cartagena, Colombia"
    ]
    SHELF_VALUES = ["A", "B", "C", "D", "E"]
    AISLE_VALUES = ["1", "2", "3", "4", "5"]
    LEVEL_VALUES = [1, 2, 3]
    ALLOWED_CATEGORIES = ["Frutas y Verduras", "Carnes y Pescados", "Lácteos y Huevos", "Panadería y Repostería", "Despensa", "Bebidas", "Snacks y Dulces", "Condimentos y Especias", "Productos de Limpieza", "Productos para Bebés"]
    def __init__(self, data, auth_token):
        self.data = data
        self.auth_token = auth_token
        self.warehouses = []
        self.quantity_warehouses = random.randint(1, 5)

    def create_warehouses(self):
        if len(self.warehouses) > 0:
            return self.warehouses
        else:
            for i in range(self.quantity_warehouses):
                warehouse = Warehouses(
                    self.WAREHOUSE_NAMES[random.randint(0, 4)],
                    self.WAREHOUSE_ADDRESSES[random.randint(0, 4)]
                )
                db_session.add(warehouse)
                db_session.commit()
                self.warehouses.append(warehouse)
            return self.warehouses
    
    def create_product_warehouse(self, product: Products):
        warehouse = random.choice(self.warehouses)
        product_warehouse = ProductWarehouse(
            product.id,
            warehouse.id,
            product.barcode,
            warehouse.name,
            warehouse.address,
            self.data['quantity'],
            random.choice(self.SHELF_VALUES),
            random.choice(self.AISLE_VALUES),
            random.choice(self.LEVEL_VALUES)
        )
        db_session.add(product_warehouse)
        db_session.commit()
                    
    def validate(self):
        errors = []

        name = self.data.get("name", "").strip()
        if not (3 <= len(name) <= 100) or not re.match(r'^[\w\s\-.]+$', name):
            errors.append(ERROR_MESSAGES["invalid_name"])

        category = self.data.get("category", "")
        if category not in self.ALLOWED_CATEGORIES:
            errors.append(ERROR_MESSAGES["invalid_category"])

        provider_id = self.data.get("provider_id", "")
        try:
            uuid.UUID(provider_id)
        except ValueError:
            errors.append(ERROR_MESSAGES["invalid_provider"])
        else:
            try:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = requests.get(f'{MANUFACTURERS}/manufacturers/{provider_id}', headers=headers)
                if response.status_code != 200:
                    errors.append(ERROR_MESSAGES["invalid_provider"])
            except ValueError:
              errors.append(ERROR_MESSAGES["invalid_provider"])

        weight = self.data.get("weight")
        if isinstance(weight, str):  
            weight = weight.replace(",", ".")
        try:
            weight = float(weight)
            if weight <= 0:
                errors.append(ERROR_MESSAGES["invalid_weight_less_than_zero"])
        except ValueError:
            errors.append(ERROR_MESSAGES["invalid_weight"])

        price = self.data.get("price")
        if isinstance(price, str):
            price = price.replace(",", ".")
        try:
            price = float(price)
        except ValueError:
            errors.append(ERROR_MESSAGES["invalid_price"])

        description = self.data.get("description", "").strip()
        if not (3 <= len(description) <= 100) or not re.match(r'^[\w\s\-.]+$', description):
            errors.append(ERROR_MESSAGES["invalid_description"])

        best_before = self.data.get("best_before", "")
        try:
            best_before_date = datetime.fromisoformat(best_before)
            if best_before_date < datetime.now():
                errors.append(ERROR_MESSAGES["invalid_best_before"])
        except ValueError:
            errors.append(ERROR_MESSAGES["invalid_date_format"])

        if errors:
            raise InvalidData(errors)

    def execute(self):
        self.validate()
        self.create_warehouses()
        try:
            with db_session.begin():
                product = Products(
                    name=self.data['name'],
                    description=self.data['description'],
                    price=float(self.data['price']),
                    category=self.data['category'],
                    weight=float(self.data['weight']),
                    barcode=self.data['barcode'],
                    provider_id=uuid.UUID(self.data['provider_id'])
                )
                db_session.add(product)
                db_session.flush()

                best_before = datetime.fromisoformat(self.data['best_before'])
                
                batch = Batches(
                    batch=self.data['batch'],
                    best_before=best_before,
                    quantity=int(self.data['quantity']),
                    product_id=product.id 
                )
                db_session.add(batch)

            self.create_product_warehouse(product)
            return {
                'id': str(product.id),
                'message': 'Producto creado exitosamente'
                }
        except Exception as e:
            db_session.rollback()
            return {'error': f'{e}Ocurrió un error al guardar el producto. Inténtelo de nuevo.'}
        finally:
            db_session.close()