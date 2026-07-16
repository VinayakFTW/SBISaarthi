import os
import httpx
from fastapi import BackgroundTasks, Request
from agents.orchestrator import Orchestrator
from database.mongo_helpers import get_active_session_for_customer
from middlewares.dependencies import validate_customer
from database.validation.message_model import MessageRequest, MessageResponse
from controllers.openwa_controllers.resolve_chat_id_to_phone import resolve_chat_id_to_phone
from controllers.openwa_controllers.get_wa_session import get_wa_session_id

orchestrator = Orchestrator()

OPENWA_URL = os.getenv("OPENWA_URL")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY")

async def process_and_reply(sender_id: str, phone_number: str, message_body: str):
    """
    Background task to run the LLM orchestrator and send the reply back via OpenWA.
    """

    req = MessageRequest(phone_number=phone_number, channel="WHATSAPP", message=message_body)
    customer = validate_customer(req)

    # 2. Manage Session and Orchestrator
    active_session = get_active_session_for_customer(customer.customer_id)
    print(f"Active session for customer {customer.customer_id}: {active_session}")
    if not active_session:
        active_session = orchestrator.start_session(customer.customer_id, req.channel)
    else:
        active_session = active_session["session_id"]

    response_text, new_state = orchestrator.process_message(active_session, message_body)

    url = f"{OPENWA_URL}/api/sessions/{get_wa_session_id()}/messages/send-text"
    payload = {
        "chatId": sender_id,
        "text": response_text, 
    }
    
    headers = {
        "X-API-Key": OPENWA_API_KEY,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload, headers=headers)
            return MessageResponse(session_id=active_session,
                                    response=response_text, 
                                    current_state=new_state)
        except Exception as e:
            return MessageResponse(session_id=active_session,
                                    response=f"Failed to send WhatsApp message: {str(e)}", 
                                    current_state=new_state)

async def openwa_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Controller logic to handle incoming OpenWA messages.
    """
    payload = await request.json()
    
    event = payload.get("event")
    data = payload.get("data", {})

    if event == "message.received" and not data.get("isGroupMsg", False):
        if data.get("fromMe", False):
            return {"status": "ignored_self_message"}
        sender_id = data.get("from")
        message_body = data.get("body")
        
        if sender_id and message_body:
            phone_number = await resolve_chat_id_to_phone(session_id=get_wa_session_id(), chat_id=sender_id)
            
            background_tasks.add_task(process_and_reply, sender_id, phone_number, message_body)

    return {"status": "received"}