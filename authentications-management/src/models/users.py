import datetime
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum, Float
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

db = SQLAlchemy()

class Role(enum.Enum):
    superadmin = 'SUPERADMIN'
    seller = 'VENDEDOR'
    client = 'CLIENTE'

class Users(Model, base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        