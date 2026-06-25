from fastapi import FastAPI, HTTPException
from database.postgres import init_db
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
    if not req.session_id:
        session_id = orchestrator.start_session(req.customer_id, req.channel)
    else:
        session_id = req.session_id

    response_text, new_state = orchestrator.process_message(session_id, req.message)
    
    return MessageResponse(
        session_id=session_id,
        response=response_text,
        current_state=new_state
    )
