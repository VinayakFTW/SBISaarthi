import os

class AccountAggregatorAdapter:
    def __init__(self):
        self.api_key = os.getenv("AA_API_KEY")

    def request_consent(self, fiu_id: str, customer_vua: str, datatypes: list, date_range: dict) -> dict:
        return {
            "consent_handle": "handle_abc", 
            "url": "https://aa.com/consent/..."
        }
