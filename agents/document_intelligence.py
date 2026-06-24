from .base_agent import BaseAgent

class DocumentIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Document Intelligence Agent",
            system_prompt=(
                "You process raw uploads (images, PDFs) and extract structured data. "
                "Fetch verified documents via DigiLocker. Re-prompt if images are blurry."
            )
        )
