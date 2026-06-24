from .base_agent import BaseAgent

class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Memory Agent",
            system_prompt=(
                "You are the historian. Manage reads and writes to the Shared Memory architecture. "
                "Extract entities, merge cross-channel context, and provide state."
            )
        )
