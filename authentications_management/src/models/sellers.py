from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum, Float, ForeignKey, UniqueConstraint
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum
from sqlalchemy.orm import relationship

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

    goals = relationship('Goals', back_populates='seller', cascade='all, delete-orphan')

    def __init__(self, name, identification, country, address, telephone, email):
        self.name = name
        self.identification = identification
        self.country = country
        self.address = address
        self.telephone = telephone
        self.email = email

class Goals(Model, base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey('sellers.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('id', 'seller_id', 'date', name='uq_goals_id_seller_date'),
    )

    seller = relationship('Sellers', back_populates='goals')

    goals_product = relationship('GoalProduct', back_populates='goal', cascade='all, delete-orphan')

    def __init__(self, seller_id, date):
        self.seller_id = seller_id
        self.date = date
        

class GoalProduct(Model, base):
    __tablename__ = 'goal_product'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    goal_id = Column(UUID(as_uuid=True), ForeignKey('goals.id'),nullable=False)
    date = Column(DateTime, nullable=False) 
    goal = relationship('Goals', back_populates='goals_product')
    sales = Column(Float, nullable=False, default=0)

    def __init__(self, product_id, quantity, goal_id, date,sales):
        self.product_id = product_id
        self.quantity = quantity
        self.goal_id = goal_id
        self.date = date
        self.sales = sales
        
