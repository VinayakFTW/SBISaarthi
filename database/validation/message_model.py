from pydantic import BaseModel

class MessageRequest(BaseModel):
    phone_number: str = None
    channel: str = "WHATSAPP"
    message: str

class MessageResponse(BaseModel):
    session_id: str
    response: str
    current_state: str