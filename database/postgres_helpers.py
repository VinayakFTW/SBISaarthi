from constants.enums import KYCStatus
from database.postgres import SessionLocal
from database.models.customer_model import Customer
from database.models.account_model import Account

from datetime import datetime, timedelta

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

def create_temp_customer(phone_number: str) -> int:
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.phone_number == phone_number).first()
        if customer:
            return customer
        new_customer = Customer(phone_number=phone_number)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_customer_by_phone(phone_number: str):
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.phone_number == phone_number).first()
        return customer
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
        
        from database.mongo_helpers import delete_sessions_for_customers
        delete_sessions_for_customers(stale_ids)
        return len(stale_ids)
    finally:
        db.close()
