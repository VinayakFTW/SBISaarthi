from .base_agent import BaseAgent
from tools.uidai import UIDAIAdapter

class KYCAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="KYC Agent",
            system_prompt=(
                "You are the meticulous verification officer. "
                "Drive the collection of identity data (Aadhaar, PAN). "
                "Initiate OTP flows using 'initiate_ekyc' when an Aadhaar is provided."
            )
        )
        self.uidai = UIDAIAdapter()
        
        self.add_tool({
            "type": "function",
            "function": {
                "name": "initiate_ekyc",
                "description": "Initiate eKYC by sending an OTP to the user's Aadhaar linked mobile number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uid": {
                            "type": "string",
                            "description": "The Aadhaar number"
                        },
                        "consent": {
                            "type": "boolean",
                            "description": "Whether the user provided consent"
                        },
                        "purpose": {
                            "type": "string",
                            "description": "The purpose of the eKYC"
                        }
                    },
                    "required": ["uid", "consent", "purpose"]
                }
            }
        }, self.uidai.initiate_ekyc)
