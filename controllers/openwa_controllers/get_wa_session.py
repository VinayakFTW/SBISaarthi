import requests
import os
from dotenv import load_dotenv
load_dotenv()

OPENWA_URL = os.getenv("OPENWA_URL")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY")

def get_wa_session_id():
    headers = {
        "X-API-Key": OPENWA_API_KEY
    }

    if requests.get(f"{OPENWA_URL}/api/sessions", headers=headers).json()[0].get("name") == "sbi-saarthi":
        response = requests.get(f"{OPENWA_URL}/api/sessions", headers=headers).json()[0].get("id")
    else:
        payload = {
            "name": "sbi-saarthi",
            "config": {"autoreconnect": True,},
            "proxyUrl":OPENWA_URL,
            "proxyType": "http",
        }

        requests.post(f"{OPENWA_URL}/api/sessions", headers=headers, json=payload)
        response = requests.get(f"{OPENWA_URL}/api/sessions", headers=headers).json()[0].get("id")

    return response
