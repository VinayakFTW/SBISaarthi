class PANVerificationAdapter:
    def __init__(self):
        pass # In reality, authenticate with NSDL/Karvy credentials here

    def verify_pan(self, pan_number: str) -> dict:
        """Mock NSDL API Call"""
        print(f"Pinging Income Tax Database for PAN: {pan_number}...")
        
        # Simulate a database lookup
        if len(pan_number) == 10 and pan_number.isalnum():
            return {
                "status": "VALID",
                "pan_status": "ACTIVE",
                "registered_name": "Ramesh Kumar", # You match this against Aadhaar
                "aadhaar_seeded": True # Checks if PAN is linked to Aadhaar (Mandatory now)
            }
        return {"status": "INVALID"}