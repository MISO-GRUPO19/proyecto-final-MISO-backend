from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.products import Products, Batch
from ..models.database import db_session
import uuid
from datetime import datetime

class CreateProducts(BaseCommand):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['name'] == '' or self.data['description'] == '' or self.data['price'] == '' or self.data['category'] == '' or self.data['weight'] == '' or self.data['barcode'] == '' or self.data['provider_id'] == '' or self.data['batch'] == '' or self.data['best_before'] == '' or self.data['quantity'] == ''):
            raise InvalidData

        try:
            with db_session.begin():
                product = Products(
                    name=self.data['name'],
                    description=self.data['description'],
                    price=self.data['price'],
                    category=self.data['category'],
                    weight=self.data['weight'],
                    barcode=self.data['barcode'],
                    provider_id=uuid.UUID(self.data['provider_id'])
                )
                db_session.add(product)
                db_session.flush()

                best_before = datetime.fromisoformat(self.data['best_before'])
                
                batch = Batch(
                    batch=self.data['batch'],
                    best_before=best_before,
                    quantity=self.data['quantity'],
                    product_id=product.id 
                )
                db_session.add(batch)
            
            return {'message': 'Producto creado exitosamente'}
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()