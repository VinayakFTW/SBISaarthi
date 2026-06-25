from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from constants.enums import KYCStatus, RiskTier

class CustomerProfile(BaseModel):
    customer_id: int
    phone_number: str
    preferred_language: str
    kyc_status: KYCStatus = KYCStatus.PENDING
    risk_tier: Optional[RiskTier] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SessionMemory(BaseModel):
    session_id: str
    customer_id: int
    channel: str
    workflow_state: str = "UNIDENTIFIED"
    messages: List[Dict[str, str]] = []
    summary: str = ""
    extracted_facts: Dict[str, Any] = {}
    agent_memories: Dict[str, Any] = {}
    retrieved_memories: List[Any] = []
    last_interaction_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLogSchema(BaseModel):
    log_id: str
    customer_id: int
    agent_id: str
    action_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cryptographic_hash: str
    metadata: Dict[str, Any] = {}
