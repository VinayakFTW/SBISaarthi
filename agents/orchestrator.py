# pyrefly: ignore [missing-import]
from tools.uidai import UIDAIAdapter
from tools.pan_verification import PANVerificationAdapter
from core.event_bus import event_bus
from core.state_machine import StateMachine, State
from database.mongo import get_session, update_session
from agents.customer_engagement import CustomerEngagementAgent
from agents.kyc import KYCAgent
from agents.document_intelligence import DocumentIntelligenceAgent
import uuid
import json

class Orchestrator:
    def __init__(self):
        self.state_machine = StateMachine()
        self.engagement_agent = CustomerEngagementAgent()
        self.kyc_agent = KYCAgent()
        self.doc_agent = DocumentIntelligenceAgent()
        
        self.uidai_adapter = UIDAIAdapter()
        self.nsdl_adapter = PANVerificationAdapter()

        # Subscribe to events
        event_bus.subscribe("USER_MESSAGE", self.handle_user_message)
        event_bus.subscribe("FETCH_PAN", self.handle_fetch_pan)
        event_bus.subscribe("FETCH_AADHAAR", self.handle_fetch_aadhaar)
        event_bus.subscribe("KYC_COMPLETED", self.handle_kyc_completed)
        
    def start_session(self, customer_id: str, channel: str):
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "customer_id": customer_id,
            "current_state": State.UNIDENTIFIED.value,
            "channel": channel,
            "collected_entities": {}
        }
        update_session(session_id, session_data)
        return session_id

    def handle_user_message(self, event_data: dict):
        session_id = event_data.get("session_id")
        message = event_data.get("message")
        
        session = get_session(session_id)
        if not session:
            print("Session not found!")
            return
            
        current_state = session.get("current_state")
        
        # Dispatch to appropriate agent based on state
        if current_state == State.UNIDENTIFIED.value:
            response = self.engagement_agent.process_message(message, context=session)
            print(f"[Engagement Agent]: {response}")
            try:
                data = json.loads(response)
                session["collected_entities"]["language"] = data.get("language")
                if self.state_machine.can_transition(current_state, State.IDENTIFIED.value):
                    session["current_state"] = State.IDENTIFIED.value
            except:
                pass
            update_session(session_id, session)

        elif current_state == State.IDENTIFIED.value:
            response = self.kyc_agent.process_message(message, context=session)
            print(f"[KYC Agent]: {response}")
            # Real implementation would parse entities and transition state

    def handle_fetch_pan(self, event_data: dict):
        session_id = event_data.get("session_id")
        session = get_session(session_id)
        if not session:
            print("Session not found!")
            return
        
        # 1. Fetch the PAN Card from NSDL
        doc_response = self.nsdl_adapter.verify_pan(pan_number=session["customer_id"])
        
        # 2. Save the verified PAN data to the session
        session["collected_entities"]["pan_verified"] = doc_response
        update_session(session_id, session)
        print(f"[Orchestrator]: Successfully fetched PAN from NSDL!")

    def handle_fetch_aadhaar(self, event_data: dict):
        session_id = event_data.get("session_id")
        session = get_session(session_id)
        if not session:
            print("Session not found!")
            return
        
        # 1. Simulate the OAuth Consent flow
        auth_response = self.uidai_adapter.initiate_ekyc(session["customer_id"], consent=True, purpose="Account Opening")
        
        # 2. Fetch the Aadhaar Card from DigiLocker
        doc_response = self.uidai_adapter.verify_otp(txn_id=auth_response["txn_id"], otp="123456")
        
        # 3. Save the verified Aadhaar data to the session
        if doc_response["status"] == "SUCCESS":
            session["collected_entities"]["aadhaar_verified"] = doc_response["demographic_data"]
            print(f"[Orchestrator]: Successfully fetched Aadhaar from UIDAI")
        else:
            session["collected_entities"]["aadhaar_verified"] = None
            print(f"[Orchestrator]: Failed to fetch Aadhaar from UIDAI")
            
        update_session(session_id, session)
    
    def handle_kyc_completed(self, event_data: dict):
        session_id = event_data.get("session_id")
        session = get_session(session_id)
        if self.state_machine.can_transition(session["current_state"], State.KYC_VERIFIED.value):
            session["current_state"] = State.KYC_VERIFIED.value
            update_session(session_id, session)
