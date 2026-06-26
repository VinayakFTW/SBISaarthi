from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

engine = create_engine(os.getenv("POSTGRES_URL", "sqlite:///./sbi_saarthi.db"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BASE = declarative_base()

from database.models.customer_model import Customer
from database.models.account_model import Account
from database.models.audit_log_model import AuditLog

def init_db():
    BASE.metadata.create_all(bind=engine)
