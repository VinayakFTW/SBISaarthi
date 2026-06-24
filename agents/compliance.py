from .base_agent import BaseAgent

class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Compliance Agent",
            system_prompt=(
                "You are the strict auditor. Ensure no regulatory steps are bypassed. "
                "Verify explicit consent logs and ensure RBI mandate compliance."
            )
        )
