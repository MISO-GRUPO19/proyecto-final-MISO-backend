import datetime
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum, Float
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Manufacturers(Model, base):
    __tablename__ = 'manufacturers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __init__(self, name, country, contact, telephone, email):
        self.name = name
        self.country = country
        self.contact = contact
        self.telephone = telephone
        self.email = email
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        