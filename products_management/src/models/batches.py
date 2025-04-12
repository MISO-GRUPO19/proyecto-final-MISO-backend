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

class Batches(Model, base):
    __tablename__ = 'batches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch = Column(String, nullable=False)
    best_before = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantityAvailable = Column(Integer, nullable=False)
    
    def __init__(self, batch, best_before, quantity, product_id):
        self.batch = batch
        self.best_before = best_before
        self.quantity = quantity
        self.product_id = product_id
        self.quantityAvailable = quantity
