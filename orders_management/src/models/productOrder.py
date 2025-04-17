from marshmallow import Schema, fields
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from .model  import  Model
from .database import base

class ProductOrder(Model, base):
    __tablename__ = 'product_order'

    product_barcode = Column(String(50), primary_key=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)


    order = relationship("Orders", back_populates="product_items")
    
    def __init__(self, product_barcode, order_id, quantity):
        self.product_barcode = product_barcode
        self.order_id = order_id
        self.quantity = quantity
    

class ProductOrderSchema(Schema):
    name = fields.Method("get_name")
    code = fields.Method("get_code")
    quantity = fields.Integer()

    def get_name(self, obj):
        return obj.product.name

    def get_code(self, obj):
        return obj.product.code
