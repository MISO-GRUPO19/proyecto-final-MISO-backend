from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, ForeignKey, String, Integer, DateTime, CheckConstraint, Enum
from .model  import  Model
from .database import base
from .productOrder import ProductOrderSchema
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from sqlalchemy.orm import relationship

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
    code = Column(String, unique=True, nullable=False)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    date_order = Column(DateTime, nullable=False)
    provider_id = Column(UUID(as_uuid=True), nullable=False)
    total = Column(Integer, nullable=False)
    type = Column(Enum(Order), nullable=False)
    state = Column(Enum(State), nullable=False)
    route_id = Column(UUID(as_uuid=True), nullable=False)

    product_items = relationship("ProductOrder", back_populates="order", cascade="all, delete-orphan")
    status_history = relationship("OrderStatusHistory", back_populates="order")
    
    def __init__(self, client_id, seller_id, date_order, provider_id, total, type, state, route_id):
        self.client_id = client_id
        self.seller_id = seller_id
        self.date_order = date_order
        self.provider_id = provider_id
        self.total = total
        self.type = type
        self.state = state
        self.route_id = route_id
        self.code = self.generate_order_code()
        
    def generate_order_code(self):
        import random
        import string
        from ..models.database import db_session

        prefix = "ORCL"
        max_attempts = 10

        for _ in range(max_attempts):
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            code = f"{prefix}{suffix}"

            existing = db_session.query(Orders).filter_by(code=code).first()
            if not existing:
                return code

class OrderStatusHistory(Model, base):
    __tablename__ = 'order_status_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    state = Column(Enum(State), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    order = relationship("Orders", back_populates="status_history")
    
    def __init__(self, order_id, state, timestamp):
        self.order_id = order_id
        self.state = state
        self.timestamp = timestamp

class OrderSchema(Schema):
    id = fields.UUID()
    state = fields.String()
    total = fields.Float()
    seller_id = fields.UUID()
    client_id = fields.UUID()
    date_order = fields.DateTime()
    product_items = fields.List(fields.Nested(ProductOrderSchema))
