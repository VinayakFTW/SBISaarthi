from sqlalchemy import Column, String, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from database.postgres import BASE

class AuditLog(BASE):
    __tablename__ = "audit_logs"

    log_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), index=True)
    agent_id = Column(String(50))
    action_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cryptographic_hash = Column(String(256))
    metadata_col = Column(JSON) 
    
    customer = relationship("Customer", back_populates="audit_logs")