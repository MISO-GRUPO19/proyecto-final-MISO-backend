from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum, Float, ForeignKey, UniqueConstraint, JSON
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import TypeDecorator
import uuid
import json

db = SQLAlchemy()

class Sellers(Model, base):
    __tablename__ = 'sellers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identification = Column(String, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    assigned_customers = Column(JSON, nullable=True, default=list)

    def __init__(self, name, identification, country, address, telephone, email, assigned_customers=None):
        self.name = name
        self.identification = identification
        self.country = country
        self.address = address
        self.telephone = telephone
        self.email = email
        self.assigned_customers = assigned_customers  

