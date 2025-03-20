import datetime
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, CheckConstraint, Enum, Float
from .model import Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class Role(enum.Enum):
    Administrador = 'Administrador'
    Vendedor = 'Vendedor'
    Cliente = 'Cliente'

class Users(Model, base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __init__(self, email, password, role):
        self.email = email
        self.set_password(password)
        self.role = role
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)