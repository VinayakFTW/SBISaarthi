import enum

class KYCStatus(enum.Enum):
    PENDING = 'PENDING'
    PARTIAL = 'PARTIAL'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'

class RiskTier(enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
