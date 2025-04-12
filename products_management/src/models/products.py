from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, String
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
    batch = relationship('Batches', backref='product', lazy=True)

    def __init__(self, name, description, price, category, weight, barcode, provider_id):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.weight = weight
        self.barcode = barcode
        self.provider_id = provider_id

