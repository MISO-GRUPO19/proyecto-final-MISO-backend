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
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    address = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __init__(self, id=None, firstName=None, lastName=None, phoneNumber=None, address=None, country=None, email=None, created_at=None, updated_at=None):
        self.id = id or uuid.uuid4()
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.address = address
        self.country = country
        self.email = email
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or datetime.datetime.utcnow()