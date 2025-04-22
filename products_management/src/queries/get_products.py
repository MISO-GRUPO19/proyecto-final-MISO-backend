from ..models.products import Products
from ..models.batches import Batches
from ..models.database import db_session
from sqlalchemy import func

class GetProducts:
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:
            productos = (
                db_session.query(
                    Products.name,
                    Products.barcode,
                    func.coalesce(func.sum(Batches.quantityAvailable), 0).label('stock'),
                    Products.price,
                    Products.category
                )
                .outerjoin(Batches, Products.id == Batches.product_id)
                .group_by(Products.name, Products.barcode, Products.price)
                .all()
            )

            products_list = []
            for p in productos:
                products_list.append({
                    'name': p.name,
                    'barcode': p.barcode,
                    'stock': int(p.stock),
                    'price': float(p.price),
                    'category': p.category
                })

            return products_list

        except Exception as e:
            return {'error': str(e)}
