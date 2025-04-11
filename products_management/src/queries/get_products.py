from ..models.products import Products, Batch, ProductOrder
from ..models.database import db_session
from sqlalchemy import func
from sqlalchemy.sql import label

class GetProducts:
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:
            subq_ordenados = (
                db_session.query(
                    ProductOrder.product_id,
                    func.coalesce(func.sum(ProductOrder.quantity), 0).label('cantidad_ordenada')
                )
                .group_by(ProductOrder.product_id)
                .subquery()
            )

            productos = (
                db_session.query(
                    func.min(Products.name).label('name'),
                    Products.barcode.label('barcode'),
                    (
                        func.coalesce(func.sum(Batch.quantity), 0) -
                        func.coalesce(func.sum(subq_ordenados.c.cantidad_ordenada), 0)
                    ).label('stock'),
                    func.min(Products.price).label('price')
                )
                .outerjoin(Batch, Products.id == Batch.product_id)
                .outerjoin(subq_ordenados, Products.id == subq_ordenados.c.product_id)
                .group_by(Products.barcode)
                .all()
            )

            products_list = []
            for p in productos:
                products_list.append({
                    'name': p.name,
                    'barcode': p.barcode,
                    'stock': p.stock,
                    'price': p.price
                })

            return products_list

        except Exception as e:
            return {'error': str(e)}
