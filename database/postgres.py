from sqlalchemy import create_engine, Column, String, Enum, DateTime, JSON, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import enum
import os
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("POSTGRES_URL", "sqlite:///./sbi_saarthi.db"))
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

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, unique=True, index=True)
    preferred_language = Column(String(10))
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.PENDING)
    risk_tier = Column(Enum(RiskTier), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    accounts = relationship("Account", back_populates="customer", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="customer", cascade="all, delete-orphan")

class Account(Base):
    __tablename__ = "accounts"
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), index=True)
    account_type = Column(String(50), default="SAVINGS")
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="accounts")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), index=True)
    agent_id = Column(String(50))
    action_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cryptographic_hash = Column(String(256))
    metadata_col = Column(JSON) 
    
    customer = relationship("Customer", back_populates="audit_logs")

def init_db():
    Base.metadata.create_all(bind=engine)

def verify_kyc_and_create_account(customer_id: int):
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer and customer.kyc_status != KYCStatus.VERIFIED:
            customer.kyc_status = KYCStatus.VERIFIED
            account = Account(customer_id=customer.customer_id, account_type="SAVINGS", balance=0.0)
            db.add(account)
            db.commit()
    finally:
        db.close()

def get_or_create_customer(phone_number: str) -> int:
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.phone_number == phone_number).first()
        if customer:
            return customer.customer_id
            
        new_customer = Customer(phone_number=phone_number)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer.customer_id
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def cleanup_stale_customers():
    db = SessionLocal()
    try:
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        stale_customers = db.query(Customer).filter(
            Customer.kyc_status != KYCStatus.VERIFIED,
            Customer.created_at < one_week_ago
        ).all()
        
        if not stale_customers:
            return 0

        stale_ids = [c.customer_id for c in stale_customers]
        
        for c in stale_customers:
            db.delete(c)
        db.commit()
        
        from database.mongo import delete_sessions_for_customers
        delete_sessions_for_customers(stale_ids)
        return len(stale_ids)
    finally:
        db.close()
