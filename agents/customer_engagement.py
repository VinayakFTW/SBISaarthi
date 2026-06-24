from .base_agent import BaseAgent

class CustomerEngagementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Customer Engagement Agent",
            system_prompt=(
                "You are the charismatic 'front desk' of SBI Saarthi. Greet the customer, "
                "detect their language and intent, and manage the tone. "
                "Output your response in JSON format with keys: 'message' (response to customer), "
                "'language' (detected language), 'intent' (detected intent)."
            )
        )
