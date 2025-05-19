import datetime
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum, Float, JSON
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Routes(Model, base):
    __tablename__ = "routes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_date = Column(DateTime, nullable=False)
    delivery_information = Column(JSON, nullable=False) 

    def __init__(self, delivery_date, delivery_information):
        self.delivery_date = delivery_date
        self.delivery_information = delivery_information