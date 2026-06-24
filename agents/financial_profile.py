from .base_agent import BaseAgent

class FinancialProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Financial Profile Agent",
            system_prompt=(
                "You are the data analyst. Build a comprehensive financial picture. "
                "Trigger Account Aggregator (AA) consent flows, parse bank statements, "
                "categorize income, and calculate cash flow."
            )
        )
