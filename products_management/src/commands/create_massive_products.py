from .base_command import BaseCommand
from ..errors.errors import NotFile
from ..models.products import Products, Batch
from ..models.database import db_session
import uuid
from datetime import datetime
import pandas as pd

class CreateMassiveProducts(BaseCommand):
    def __init__(self, file):
        self.file = file
    
    def execute(self):
        
        if self.file.filename == '':
            raise NotFile

        try:
            with db_session.begin():

                df = pd.read_excel(self.file)
                products = []
                
                for index, row in df.iterrows():
                    product = Products(
                        name=row['name'],
                        description=row['description'],
                        price=row['price'],
                        category=row['category'],
                        weight=row['weight'],
                        barcode=row['barcode'],
                        provider_id=uuid.UUID(row['provider_id'])
                    )
                    products.append(product)
                    
                db_session.add_all(products)
                db_session.flush() 

                batches = []
                for index, row in df.iterrows():
                    product = next((p for p in products if p.name == row['name']), None)
                    if product:
                        batch = Batch(
                            batch=row['batch'],
                            best_before=row['best_before'],
                            quantity=row['quantity'],
                            product_id=product.id 
                        )
                        batches.append(batch)
                    
                db_session.add_all(batches)
                db_session.commit()
            return {'message': 'Productos creados correctamente'}
            
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()