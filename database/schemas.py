from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class KYCStatus(str, Enum):
    PENDING = 'PENDING'
    PARTIAL = 'PARTIAL'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'

class RiskTier(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class CustomerProfile(BaseModel):
    customer_id: str
    phone_number: str
    preferred_language: str
    kyc_status: KYCStatus = KYCStatus.PENDING
    risk_tier: Optional[RiskTier] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SessionState(BaseModel):
    session_id: str
    customer_id: str
    current_state: str
    channel: str
    collected_entities: Dict[str, Any] = {}
    last_interaction_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLogSchema(BaseModel):
    log_id: str
    customer_id: str
    agent_id: str
    action_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cryptographic_hash: str
    metadata: Dict[str, Any] = {}
