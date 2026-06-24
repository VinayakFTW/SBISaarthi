from .base_agent import BaseAgent

class CreditUnderwritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Credit Underwriting Agent",
            system_prompt=(
                "You are the loan officer. Use the financial profile to recommend products. "
                "Calculate risk scores, assess loan eligibility, and generate pre-approved offers."
            )
        )
