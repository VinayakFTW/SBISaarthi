from fastapi import FastAPI
from controllers.chat_endpoints import chat
from database.validation.message_model import MessageRequest, MessageResponse

app = FastAPI(title="SBI Saarthi API Gateway")

app.add_api_route(
    path="/api/v1/chat", 
    endpoint=chat, 
    methods=["POST"], 
    response_model=MessageResponse
)
