from enum import Enum
from typing import Dict, List

class State(str, Enum):
    UNIDENTIFIED = "UNIDENTIFIED"
    IDENTIFIED = "IDENTIFIED"
    KYC_INITIATED = "KYC_INITIATED"
    KYC_VERIFIED = "KYC_VERIFIED"
    PROFILED = "PROFILED"
    RISK_ASSESSED = "RISK_ASSESSED"
    PENDING_HUMAN_APPROVAL = "PENDING_HUMAN_APPROVAL"
    ACCOUNT_ACTIVE = "ACCOUNT_ACTIVE"
    CREDIT_EVALUATED = "CREDIT_EVALUATED"

class StateMachine:
    def __init__(self):
        self.transitions: Dict[State, List[State]] = {
            State.UNIDENTIFIED: [State.IDENTIFIED],
            State.IDENTIFIED: [State.KYC_INITIATED],
            State.KYC_INITIATED: [State.KYC_VERIFIED],
            State.KYC_VERIFIED: [State.PROFILED],
            State.PROFILED: [State.RISK_ASSESSED],
            State.RISK_ASSESSED: [State.PENDING_HUMAN_APPROVAL],
            State.PENDING_HUMAN_APPROVAL: [State.ACCOUNT_ACTIVE],
            State.ACCOUNT_ACTIVE: [State.CREDIT_EVALUATED],
        }

    def can_transition(self, current_state: str, next_state: str) -> bool:
        try:
            curr = State(current_state)
            nxt = State(next_state)
            return nxt in self.transitions.get(curr, [])
        except ValueError:
            return False
