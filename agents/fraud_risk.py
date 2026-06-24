from .base_agent import BaseAgent

class FraudRiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Fraud & Risk Agent",
            system_prompt=(
                "You are the silent security guard. "
                "Validate liveness, detect voice deepfakes, analyze behavioral biometrics, "
                "and cross-reference identity watchlists."
            )
        )
