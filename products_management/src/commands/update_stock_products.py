import logging
from ..models.database import db_session
from sqlalchemy import func
from ..models.products import Products
from ..models.batches import Batches
from ..errors.errors import InvalidData, ProductInsufficientStock, ProductNotFound
from .base_command import BaseCommand
from flask import jsonify

class UpdateStockProducts(BaseCommand):
    def __init__(self, barcode, quantity):
        self.barcode = barcode
        self.quantity = int(quantity) 
        
    def execute(self):
        if not self.barcode:
            raise InvalidData

        try:
            products = (
                db_session.query(Products)
                .filter(Products.barcode == self.barcode)
                .all()
            )

            if not products:
                raise ProductNotFound

            product_ids = [p.id for p in products]

            total_stock = (
                db_session.query(func.coalesce(func.sum(Batches.quantityAvailable), 0))
                .filter(Batches.product_id.in_(product_ids))
                .scalar()
            )

            logging.info(f"Total stock for product {total_stock}")
            logging.info(f"Requested quantity: {self.quantity}")

            cantidad_solicitada = self.quantity
            if total_stock < cantidad_solicitada:
                raise ProductInsufficientStock

            cantidad_restante = cantidad_solicitada
            lotes = (
                db_session.query(Batches)
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

            db_session.commit()

            return {
                "barcode": self.barcode,
                "requested_quantity": cantidad_solicitada,
                "remaining_stock": total_stock - cantidad_solicitada
            }

        except ProductNotFound:
            return jsonify({"error": "ProductNotFound", "barcode": self.barcode}), 404
        except ProductInsufficientStock:
            return jsonify({"error": "ProductInsufficientStock", "barcode": self.barcode}), 400
        except Exception as e:
            db_session.rollback()
            logging.error(f"Error interno: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
        finally:
            db_session.remove()
