import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from .model import Model
from .database import base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Stores(Model, base):
    __tablename__ = 'stores'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)  # Correctamente definido aquí
    address = Column(String, nullable=False)
    store_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    customer = relationship("Customers", back_populates="stores")

    def __init__(self, id=None, customer_id=None, address=None, store_name=None, created_at=None, updated_at=None):
        self.id = id or uuid.uuid4()
        self.customer_id = customer_id
        self.address = address
        self.store_name = store_name
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or datetime.datetime.utcnow()