from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .model import Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class ProductWarehouse(Model, base):
    __tablename__ = 'product_warehouse'

    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey('warehouses.id'), primary_key=True)
    product_barcode = Column(String, nullable=False)
    warehouse_name = Column(String, nullable=False)
    warehouse_address = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    shelf = Column(String, nullable=False)  
    aisle = Column(String, nullable=False)  
    level = Column(Integer, nullable=False)  

    
    product = relationship('Products', backref='product_warehouse_relationships')
    warehouse = relationship('Warehouses', backref='product_warehouse_relationships')
    def __init__(self, product_id, warehouse_id, product_barcode, warehouse_name, warehouse_address,quantity, shelf, aisle, level):
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.product_barcode = product_barcode
        self.warehouse_name = warehouse_name
        self.warehouse_address = warehouse_address
        self.quantity = quantity
        self.shelf = shelf
        self.aisle = aisle
        self.level = level


class Products(Model, base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    barcode = Column(String, nullable=False)
    provider_id = Column(UUID(as_uuid=True), nullable=False)
    batch = relationship('Batches', backref='product', lazy=True)

    
    warehouses = relationship('Warehouses', secondary='product_warehouse', back_populates='products')

    def __init__(self, name, description, price, category, weight, barcode, provider_id):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.weight = weight
        self.barcode = barcode
        self.provider_id = provider_id


class Warehouses(Model, base):
    __tablename__ = 'warehouses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    
    products = relationship('Products', secondary='product_warehouse', back_populates='warehouses')

    def __init__(self, name, address):
        self.name = name
        self.address = address
