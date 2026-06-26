import requests

def get_wa_chat_history(API_KEY, API_BASE_URL, session_id=None, chat_id=None):
    headers = {
        "X-API-Key": API_KEY
    }

    response = requests.post(f"{API_BASE_URL}/api/sessions/{session_id}/messages/{chat_id}/history", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
