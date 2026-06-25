from pydantic import BaseModel

class MessageRequest(BaseModel):
    customer_id: str
    channel: str = "WHATSAPP"
    session_id: str = None
    message: str

class MessageResponse(BaseModel):
    session_id: str
    response: str
    current_state: str