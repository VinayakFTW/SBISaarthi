from sqlalchemy import create_engine, Column, String, Enum, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import enum
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Fallback to sqlite for local testing if Postgres is not available
POSTGRES_URL = os.getenv("POSTGRES_URL", "sqlite:///./sbi_saarthi.db")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class KYCStatus(enum.Enum):
    PENDING = 'PENDING'
    PARTIAL = 'PARTIAL'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'

class RiskTier(enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String, unique=True, index=True)
    preferred_language = Column(String(10))
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.PENDING)
    risk_tier = Column(Enum(RiskTier), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, index=True)
    agent_id = Column(String(50))
    action_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cryptographic_hash = Column(String(256))
    metadata_col = Column(JSON) 

def init_db():
    Base.metadata.create_all(bind=engine)
