from .base_agent import BaseAgent

class AccessibilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Accessibility Agent",
            system_prompt=(
                "You analyze interaction patterns to detect low literacy or accessibility needs. "
                "Recommend switches to 'Voice-First Mode' or trigger ISL 3D avatars as needed."
            )
        )
