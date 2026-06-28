import requests
import os
from dotenv import load_dotenv
load_dotenv()

OPENWA_URL = os.getenv("OPENWA_URL")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY")


def get_wa_chat_last_message(session_id=None, chat_id=None):
    headers = {
        "X-API-Key": OPENWA_API_KEY
    }
    if session_id is None or chat_id is None:
        return None
    response = requests.get(f"{OPENWA_URL}/api/sessions/{session_id}/messages/{chat_id}/history", headers=headers)
    if response.status_code == 200:
        return response.json()[-1].get("body")
    else:
        return None
