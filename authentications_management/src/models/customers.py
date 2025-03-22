import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime
from .model import Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Customers(Model, base):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __init__(self, name, country, address, telephone, email):
        self.name = name
        self.country = country
        self.address = address
        self.telephone = telephone
        self.email = email
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()