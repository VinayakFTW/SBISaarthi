from .base_agent import BaseAgent

class TrustEducationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Trust & Education Agent",
            system_prompt=(
                "You are the empathetic guide. Detect user hesitation or confusion. "
                "Explain why data is needed (e.g., 'We need your Aadhaar to keep your money safe')."
            )
        )
