from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from .model  import  Model
import enum
from .database import base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy() 

class VideoStatus(enum.Enum):
    processing = "PROCESANDO"
    processed = "PROCESADO"
    failed = "FALLIDO"

class Video(Model, base):
    __tablename__ = 'videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fileInfo = Column(String, nullable=False)
    name = Column(String, nullable=False)
    visitId = Column(UUID(as_uuid=True), nullable=False)
    status = Column(Enum(VideoStatus), default=VideoStatus.processing)
    results = Column(JSON, nullable=True)
    

    def __init__(self, fileInfo, name, visitId, status):
        self.fileInfo = fileInfo
        self.name = name
        self.visitId = visitId
        self.status = status
        