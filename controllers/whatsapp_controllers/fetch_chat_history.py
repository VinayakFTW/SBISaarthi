import requests

def get_wa_chat_last_message(API_KEY, API_BASE_URL, session_id=None, chat_id=None):
    headers = {
        "X-API-Key": API_KEY
    }
    if session_id is None or chat_id is None:
        return None
    response = requests.get(f"{API_BASE_URL}/api/sessions/{session_id}/messages/{chat_id}/history", headers=headers)
    if response.status_code == 200:
        return response.json()[-1].get("body")
    else:
        return None
