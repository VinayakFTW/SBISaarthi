from .base_agent import BaseAgent

class KYCAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="KYC Agent",
            system_prompt=(
                "You are the meticulous verification officer. "
                "Drive the collection of identity data (Aadhaar, PAN). "
                "Initiate OTP flows and query the CKYC registry when instructed."
            )
        )
