from .base_agent import BaseAgent

class HumanOfficerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Human Officer Agent",
            system_prompt=(
                "You bridge the AI to the human branch manager. Compile a concise 'Decision Package' "
                "(Summary, KYC status, Fraud Score, Financial Profile). Present this for final 1-click approval."
            )
        )
