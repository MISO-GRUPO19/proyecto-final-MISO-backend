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

class Goals(Model, base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    date = Column(DateTime, nullable=False)

    '''
    __table_args__ = (
        UniqueConstraint('id', 'seller_id', 'date', name='uq_goals_id_seller_date'),
    )

    seller = relationship('Sellers', back_populates='goals')
    '''
    goals_product = relationship('GoalProduct', back_populates='goal', cascade='all, delete-orphan')

    def __init__(self, seller_id, date):
        self.seller_id = seller_id
        self.date = date
        

class GoalProduct(Model, base):
    __tablename__ = 'goal_product'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_barcode = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    goal_id = Column(UUID(as_uuid=True), ForeignKey('goals.id'),nullable=False)
    date = Column(DateTime, nullable=False) 
    goal = relationship('Goals', back_populates='goals_product')
    sales = Column(Float, nullable=True, default=0)
    sales_expectation = Column(Float, nullable=False, default=0)

    def __init__(self, product_barcode, quantity, goal_id, date, sales_expectation):
        self.product_barcode = product_barcode
        self.quantity = quantity
        self.goal_id = goal_id
        self.date = date
        self.sales_expectation = sales_expectation
        
