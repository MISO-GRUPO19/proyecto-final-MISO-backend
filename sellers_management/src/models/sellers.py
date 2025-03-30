from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy  import  Column, String, Integer, DateTime, CheckConstraint, Enum, Float
from .model  import  Model
from .database import base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum

db = SQLAlchemy()

class CountryEnum(Enum):
    ARGENTINA = "Argentina"
    BOLIVIA = "Bolivia"
    BRAZIL = "Brazil"
    CANADA = "Canada"
    CHILE = "Chile"
    COLOMBIA = "Colombia"
    COSTA_RICA = "Costa Rica"
    CUBA = "Cuba"
    DOMINICAN_REPUBLIC = "Dominican Republic"
    ECUADOR = "Ecuador"
    EL_SALVADOR = "El Salvador"
    GUATEMALA = "Guatemala"
    HAITI = "Haiti"
    HONDURAS = "Honduras"
    JAMAICA = "Jamaica"
    MEXICO = "Mexico"
    NICARAGUA = "Nicaragua"
    PANAMA = "Panama"
    PARAGUAY = "Paraguay"
    PERU = "Peru"
    UNITED_STATES = "United States"
    URUGUAY = "Uruguay"
    VENEZUELA = "Venezuela"
class Sellers(Model, base):
    __tablename__ = 'sellers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identification = Column(String, nullable=False)
    name = Column(String, nullable=False)
    country = Column(Enum(CountryEnum), nullable=False, native_enum=False)
    address = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __init__(self, name, identification, country, address, telephone, email):
        self.name = name
        self.identification = identification
        self.country = country
        self.address = address
        self.telephone = telephone
        self.email = email
        