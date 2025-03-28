from datetime import datetime
from sqlalchemy import Column, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Model:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    