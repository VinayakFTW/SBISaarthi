import requests
import os
from dotenv import load_dotenv
load_dotenv()

OPENWA_URL = os.getenv("OPENWA_URL")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY")

def get_wa_session_chats(session_id=None):
    headers = {
        "X-API-Key": OPENWA_API_KEY
    }

    if session_id:
        response = requests.get(f"{OPENWA_URL}/api/sessions/{session_id}/chats", headers=headers)
        if response.status_code == 200:
            result = []
            for obj in response.json():
                if not obj.get("isGroup"):
                    result.append({"chat_name": obj.get("name")})
            return result
        else:
            return None
    else:
        return None
