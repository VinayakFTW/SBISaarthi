from database.validation.message_model import MessageRequest
from database.postgres_helpers import get_customer_by_phone,create_temp_customer

import os
from dotenv import load_dotenv

load_dotenv()

def validate_customer(req: MessageRequest):
    """
    Dependency to check if the customer exists before processing the chat.
    """
    if os.getenv("MODE") == "development":
        # In development mode, use random number configure in your .env
        req.phone_number = os.getenv("MOCK_NUM")

    customer = get_customer_by_phone(req.phone_number)
    
    if not customer:
        customer = create_temp_customer(req.phone_number)
    
    return customer