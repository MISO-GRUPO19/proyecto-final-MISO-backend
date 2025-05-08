from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, ForeignKey, String, Integer, DateTime, CheckConstraint, Enum
from .model  import  Model
from .database import base
from .productOrder import ProductOrderSchema
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

db = SQLAlchemy()

class Visits(Model, base):
    __tablename__ = 'visits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    visit_date = Column(DateTime, nullable=False)

    def __init__(self, seller_id, customer_id, visit_date):
        self.seller_id = seller_id
        self.customer_id = customer_id
        self.visit_date = visit_date