from database.mongo_helpers import get_active_session_for_customer
from middlewares.dependencies import validate_customer
from database.validation.message_model import MessageRequest, MessageResponse
from agents.orchestrator import Orchestrator
from fastapi import Depends

orchestrator = Orchestrator()

def chat(req: MessageRequest,customer=Depends(validate_customer)):    
    active_session = get_active_session_for_customer(customer.customer_id)

    if not active_session:
        session_id = orchestrator.start_session(customer.customer_id, req.channel)
    else:
        session_id = active_session["session_id"]

    response_text, new_state = orchestrator.process_message(session_id, req.message)
    
    return MessageResponse(
        session_id=session_id,
        response=response_text,
        current_state=new_state
    )