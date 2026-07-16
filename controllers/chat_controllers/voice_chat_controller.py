#voice chat controller

from database.mongo_helpers import get_active_session_for_customer
from middlewares.dependencies import validate_customer
from database.validation.message_model import MessageRequest, MessageResponse
from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

async def process_and_reply_voice_chat(phone_number: str, message_body: str) -> MessageResponse:
    """
    Process the incoming voice chat message and generate a response.
    """
    req = MessageRequest(phone_number=phone_number, channel="VOICE_CHAT", message=message_body)
    customer = validate_customer(req)

    # Manage Session and Orchestrator
    active_session = get_active_session_for_customer(customer.customer_id)
    print(f"Active session for customer {customer.customer_id}: {active_session}")
    if not active_session:
        active_session = orchestrator.start_session(customer.customer_id, req.channel)
    else:
        active_session = active_session["session_id"]

    response_text, new_state = orchestrator.process_message(active_session, message_body)

    return MessageResponse(session_id=active_session
                           ,response=response_text
                           ,current_state=new_state)
