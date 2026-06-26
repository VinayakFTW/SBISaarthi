from core.state_machine import StateMachine, State
from database.mongo_helpers import get_session, update_session, clear_session
from agents.customer_engagement import CustomerEngagementAgent
from agents.kyc import KYCAgent
from agents.financial_profile import FinancialProfileAgent
import uuid
import json
import re
from datetime import datetime

class Orchestrator:
    def __init__(self):
        self.state_machine = StateMachine()
        self.engagement_agent = CustomerEngagementAgent()
        self.kyc_agent = KYCAgent()
        self.financial_agent = FinancialProfileAgent()
        
    def start_session(self, customer_id: int, channel: str):
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "customer_id": customer_id,
            "channel": channel,
            "workflow_state": State.UNIDENTIFIED.value,
            "messages": [],
            "summary": "",
            "extracted_facts": {},
            "agent_memories": {},
            "retrieved_memories": []
        }
        update_session(session_id, session_data)
        return session_id

    def build_context(self, session: dict, agent_name: str) -> dict:
        return {
            "summary": session.get("summary", ""),
            "facts": session.get("extracted_facts", {}),
            "workflow": session.get("workflow_state", ""),
            "agent_memory": session.get("agent_memories", {}).get(agent_name, {}),
            "latest_messages": session.get("messages", [])[-5:]
        }

    def process_message(self, session_id: str, message: str) -> tuple[str, str]:
        session = get_session(session_id)
        if not session:
            return "Session not found.", State.UNIDENTIFIED.value
            
        current_state = session.get("workflow_state", State.UNIDENTIFIED.value)
        final_responses = []
        
        # Add user message to persistent memory
        messages_history = session.get("messages", [])
        messages_history.append({"role": "user", "content": message, "timestamp": str(datetime.utcnow())})
        session["messages"] = messages_history
        
        try:
            # Fast-track check
            if current_state in [State.UNIDENTIFIED.value, State.IDENTIFIED.value]:
                if re.search(r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b', message):
                    session["workflow_state"] = State.KYC_INITIATED.value
                    current_state = State.KYC_INITIATED.value

            if current_state == State.UNIDENTIFIED.value:
                context = self.build_context(session, "customer_engagement")
                response = self.engagement_agent.process_message(message, context=context)
                response_text = response
                
                try:
                    cleaned = response.strip().strip("```json").strip("```").strip()
                    data = json.loads(cleaned)
                    if "message" in data:
                        response_text = data["message"]
                    if "language" in data:
                        session["extracted_facts"]["language"] = data["language"]
                except Exception:
                    pass
                
                if self.state_machine.can_transition(current_state, State.IDENTIFIED.value):
                    session["workflow_state"] = State.IDENTIFIED.value

                final_responses.append(response_text)

            elif current_state == State.IDENTIFIED.value or current_state == State.KYC_INITIATED.value:
                if current_state == State.IDENTIFIED.value and self.state_machine.can_transition(current_state, State.KYC_INITIATED.value):
                    session["workflow_state"] = State.KYC_INITIATED.value
                    
                context = self.build_context(session, "kyc")
                response_text = self.kyc_agent.process_message(message, context=context)
                
                if "otp" in response_text.lower() or "sent" in response_text.lower():
                     if self.state_machine.can_transition(session["workflow_state"], State.KYC_VERIFIED.value):
                         session["workflow_state"] = State.KYC_VERIFIED.value
                         from database.postgres import verify_kyc_and_create_account
                         verify_kyc_and_create_account(session["customer_id"])
                         
                final_responses.append(response_text)
            
            elif current_state == State.KYC_VERIFIED.value:
                 context = self.build_context(session, "financial_profile")
                 response_text = self.financial_agent.process_message(message, context=context)
                 final_responses.append(response_text)
                 
        except Exception as e:
            final_responses.append(f"An error occurred while processing: {str(e)}")
            
        combined_response = "\n\n".join([r for r in final_responses if r])
        
        # Append AI response to persistent memory
        session["messages"].append({"role": "assistant", "content": combined_response, "timestamp": str(datetime.utcnow())})
        
        update_session(session_id, session)
        return combined_response, session["workflow_state"]
        
    def clear_session_memory(self, session_id: str):
        clear_session(session_id)
