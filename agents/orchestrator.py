from core.event_bus import event_bus
from core.state_machine import StateMachine, State
from database.mongo import get_session, update_session
from agents.customer_engagement import CustomerEngagementAgent
from agents.kyc import KYCAgent
import uuid
import json

class Orchestrator:
    def __init__(self):
        self.state_machine = StateMachine()
        self.engagement_agent = CustomerEngagementAgent()
        self.kyc_agent = KYCAgent()
        
        # Subscribe to events
        event_bus.subscribe("USER_MESSAGE", self.handle_user_message)
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
            
    def handle_kyc_completed(self, event_data: dict):
        session_id = event_data.get("session_id")
        session = get_session(session_id)
        if self.state_machine.can_transition(session["current_state"], State.KYC_VERIFIED.value):
            session["current_state"] = State.KYC_VERIFIED.value
            update_session(session_id, session)
