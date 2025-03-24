from typing import List
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .model import Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

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
    batch = relationship('Batch', backref='product', lazy=True)

    def __init__(self, name, description, price, category, weight, barcode, provider_id):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.weight = weight
        self.barcode = barcode
        self.provider_id = provider_id

class Batch(Model, base):
    __tablename__ = 'batches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch = Column(String, nullable=False)
    best_before = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    
    def __init__(self, batch, best_before, quantity, product_id):
        self.batch = batch
        self.best_before = best_before
        self.quantity = quantity
        self.product_id = product_id
        
class Category(Model, base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name
        
class Provider(Model, base):
    __tablename__ = 'providers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable = False)

    def __init__(self, name, country, contact, telephone, email):
        self.name = name
        self.country = country
        self.contact = contact
        self.telephone = telephone
        self.email = email
