from pydantic import BaseModel
from typing import Optional

class MessageRequest(BaseModel):
    identifier: str
    channel: str = "WHATSAPP"
    message: str

class MessageResponse(BaseModel):
    session_id: str
    response: str
    current_state: str