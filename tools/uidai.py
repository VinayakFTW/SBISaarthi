import os

class UIDAIAdapter:
    def __init__(self):
        self.api_key = os.getenv("UIDAI_API_KEY")

    def initiate_ekyc(self, uid: str, consent: bool, purpose: str) -> dict:
        print(f"Calling UIDAI API with UID: {uid}...")
        return {
            "txn_id": "tx123", 
            "status": "OTP_SENT"
        }

    def verify_otp(self, txn_id: str, otp: str) -> dict:
        return {
            "status": "SUCCESS",
            "demographic_data": {
                "name": "Ramesh Kumar",
                "dob": "1980-01-01",
                "address": "Village XYZ, District ABC, State DEF"
            }
        }
