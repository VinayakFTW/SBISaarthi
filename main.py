from fastapi import FastAPI, HTTPException
from database.postgres import init_db, get_or_create_customer
from database.mongo import get_active_session_for_customer
from models.message_model import MessageRequest, MessageResponse
from agents.orchestrator import Orchestrator
import uvicorn

app = FastAPI(title="SBI Saarthi API Gateway")
orchestrator = Orchestrator()

@app.on_event("startup")
def on_startup():
    print("Initializing Database...")
    init_db()

@app.post("/chat", response_model=MessageResponse)
def chat_endpoint(req: MessageRequest):
    # 1. Look up or create the customer based on their channel identifier (e.g., WhatsApp phone number)
    customer_id = get_or_create_customer(req.identifier)
    
    # 2. Look up the active session for this customer
    active_session = get_active_session_for_customer(customer_id)
    
    if not active_session:
        session_id = orchestrator.start_session(customer_id, req.channel)
    else:
        session_id = active_session["session_id"]

    # 3. Process the message
    response_text, new_state = orchestrator.process_message(session_id, req.message)
    
    return MessageResponse(
        session_id=session_id,
        response=response_text,
        current_state=new_state
    )
