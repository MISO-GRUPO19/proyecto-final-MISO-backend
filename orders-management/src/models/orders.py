from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

db = SQLAlchemy()

class Order(enum.Enum):
    PROVEEDOR = 'PROVEEDOR'
    CLIENTE = 'CLIENTE'
    
    
class State(enum.Enum):
    PENDIENTE = 'PENDIENTE'
    ENPORCESO = 'EN PROCESO'
    ENTREGADO = 'ENTREGADO'
    CANCELADO = 'CANCELADO'
    
class TypeClient(enum.Enum):
    TIENDA = 'TIENDA'
    SUPERMERCADO = 'SUPERMERCADO'
    AUTOSERVICIO = 'AUTOSERVICIO'
    

class Orders(Model, base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    date_order = Column(DateTime, nullable=False)
    provider_id = Column(UUID(as_uuid=True), nullable=False)
    total = Column(Integer, nullable=False)
    type = Column(Enum(Order), nullable=False)
    state = Column(Enum(State), nullable=False)
    route_id = Column(UUID(as_uuid=True), nullable=False)
    products = Column(String, nullable=False)

    def __init__(self, client_id, seller_id, date_order, provider_id, total, type, state, route_id, products):
        self.client_id = client_id
        self.seller_id = seller_id
        self.date_order = date_order
        self.provider_id = provider_id
        self.total = total
        self.type = type
        self.state = state
        self.route_id = route_id
        self.products = products