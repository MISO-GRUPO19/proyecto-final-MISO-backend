import logging
from ..models.database import db_session
from sqlalchemy import func
from ..models.products import Products
from ..models.batches import Batches
from ..errors.errors import InvalidData
from .base_command import BaseCommand

class UpdateStockProducts(BaseCommand):
    def __init__(self, barcode, quantity):
        self.barcode = barcode
        self.quantity = int(quantity) 
        
    def execute(self):
        if not all([self.barcode]):
            raise InvalidData
        
        try:
            with db_session() as session:

                products = (
                    session.query(Products)
                    .filter(Products.barcode == self.barcode)
                    .all()
                )

                if not products:
                    raise InvalidData("No se encontraron productos con ese código de barras")

                product_ids = [p.id for p in products]

                # Sumar el stock total de todos los lotes asociados a esos productos
                total_stock = (
                    session.query(func.coalesce(func.sum(Batches.quantityAvailable), 0))
                    .filter(Batches.product_id.in_(product_ids))
                    .scalar()
                )

                logging.info(f"Total stock for product {total_stock}")
                logging.info(f"Requested quantity: {self.quantity}")

                cantidad_solicitada = self.quantity
                if total_stock < cantidad_solicitada:
                    raise InvalidData(f"No hay suficiente stock disponible. Disponible: {total_stock}")

                # Reducir cantidad usando lotes FIFO (más próximos a vencer primero)
                cantidad_restante = cantidad_solicitada
                lotes = (
                    session.query(Batches)
                    .filter(Batches.product_id.in_(product_ids), Batches.quantityAvailable > 0)
                    .order_by(Batches.best_before.asc())
                    .all()
                )

                for lote in lotes:
                    if cantidad_restante <= 0:
                        break
                    if lote.quantityAvailable >= cantidad_restante:
                        lote.quantityAvailable -= cantidad_restante
                        cantidad_restante = 0
                    else:
                        cantidad_restante -= lote.quantityAvailable
                        lote.quantityAvailable = 0

                session.commit()

                return {
                    "barcode": self.barcode,
                    "requested_quantity": cantidad_solicitada,
                    "remaining_stock": total_stock - cantidad_solicitada
                }

        
        except Exception as e:
            session.rollback()
            raise InvalidData(f"Error al actualizar el producto: {str(e)}")