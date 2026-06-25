from .base_agent import BaseAgent
from tools.account_aggregator import AccountAggregatorAdapter

class FinancialProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Financial Profile Agent",
            system_prompt=(
                "You are the data analyst. Build a comprehensive financial picture. "
                "Trigger Account Aggregator (AA) consent flows using 'request_consent', parse bank statements, "
                "categorize income, and calculate cash flow."
            )
        )
        self.aa_adapter = AccountAggregatorAdapter()
        
        self.add_tool({
            "type": "function",
            "function": {
                "name": "request_consent",
                "description": "Request Account Aggregator consent from the user to fetch financial data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fiu_id": {"type": "string"},
                        "customer_vua": {"type": "string"},
                        "datatypes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "date_range": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "string"},
                                "end": {"type": "string"}
                            }
                        }
                    },
                    "required": ["fiu_id", "customer_vua", "datatypes", "date_range"]
                }
            }
        }, self.aa_adapter.request_consent)
