from sqlalchemy import Column, String, Enum, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from database.postgres import BASE
from constants.enums import KYCStatus, RiskTier

class Customer(BASE):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, unique=True, index=True)
    preferred_language = Column(String(10))
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.PENDING)
    risk_tier = Column(Enum(RiskTier), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    accounts = relationship("Account", back_populates="customer", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="customer", cascade="all, delete-orphan")
