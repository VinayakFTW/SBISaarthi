from core.state_machine import StateMachine, State
from database.mongo import get_session, update_session
from agents.customer_engagement import CustomerEngagementAgent
from agents.kyc import KYCAgent
from agents.financial_profile import FinancialProfileAgent
import uuid
import json

class Orchestrator:
    def __init__(self):
        self.state_machine = StateMachine()
        self.engagement_agent = CustomerEngagementAgent()
        self.kyc_agent = KYCAgent()
        self.financial_agent = FinancialProfileAgent()
        
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

    def process_message(self, session_id: str, message: str) -> tuple[str, str]:
        session = get_session(session_id)
        if not session:
            return "Session not found.", State.UNIDENTIFIED.value
            
        current_state = session.get("current_state", State.UNIDENTIFIED.value)
        response_text = ""
        
        try:
            if current_state == State.UNIDENTIFIED.value:
                response = self.engagement_agent.process_message(message, context=session)
                response_text = response
                
                # Robust parsing of JSON from engagement agent
                try:
                    cleaned = response.strip().strip("```json").strip("```").strip()
                    data = json.loads(cleaned)
                    if "message" in data:
                        response_text = data["message"]
                    if "language" in data:
                        session["collected_entities"]["language"] = data["language"]
                        
                    # Transition State
                    if self.state_machine.can_transition(current_state, State.IDENTIFIED.value):
                        session["current_state"] = State.IDENTIFIED.value
                except Exception as e:
                    pass
                    
            elif current_state == State.IDENTIFIED.value or current_state == State.KYC_INITIATED.value:
                if current_state == State.IDENTIFIED.value and self.state_machine.can_transition(current_state, State.KYC_INITIATED.value):
                    session["current_state"] = State.KYC_INITIATED.value
                    
                response_text = self.kyc_agent.process_message(message, context=session)
                
                # State hook based on agent output
                if "verified" in response_text.lower() or "successful" in response_text.lower():
                     if self.state_machine.can_transition(session["current_state"], State.KYC_VERIFIED.value):
                         session["current_state"] = State.KYC_VERIFIED.value
            
            elif current_state == State.KYC_VERIFIED.value:
                 response_text = self.financial_agent.process_message(message, context=session)

            else:
                 response_text = "Your request is currently being processed by our system."
                 
        except Exception as e:
            response_text = f"An error occurred while processing: {str(e)}"
            
        update_session(session_id, session)
        return response_text, session["current_state"]
