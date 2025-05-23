import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Boolean
from .model import Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Customers(Model, base):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    address = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, nullable=False)
    seller_assigned = Column(UUID(as_uuid=True), nullable=True, default=None)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __init__(self, firstName, lastName, phoneNumber, address, country, email, seller_assigned=None):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.address = address
        self.country = country
        self.email = email
        self.seller_assigned = seller_assigned
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()