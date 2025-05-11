from ..models.products import Products
from ..models.batches import Batches
from ..models.database import db_session
from sqlalchemy import func
from flask import jsonify
from ..errors.errors import *

class GetProductValidate:
    def __init__(self, barcode, quantity, token):
        self.barcode = barcode
        self.quantity = int(quantity) 
        self.token = token

    def execute(self):
        try:
            product = (
                db_session.query(
                    Products.name,
                    Products.barcode,
                    func.coalesce(func.sum(Batches.quantityAvailable), 0).label('stock'),
                    Products.price
                )
                .outerjoin(Batches, Products.id == Batches.product_id)
                .group_by(Products.name, Products.barcode, Products.price)
                .filter(Products.barcode == self.barcode)
                .all()
            )

            if not product:
                raise ProductNotFound
            
            if product[0].stock < self.quantity:
                raise ProductInsufficientStock
            
            return jsonify({
                'product_name': product[0].name,
                'product_barcode': product[0].barcode,
                'product_stock': product[0].stock,
                'product_price': product[0].price
            }), 200

        except ProductNotFound:
            return jsonify({"error": "ProductNotFound", "barcode": self.barcode}), 404
        except ProductInsufficientStock:
            return jsonify({"error": "ProductInsufficientStock", "barcode": self.barcode}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
        finally:
            db_session.remove()
