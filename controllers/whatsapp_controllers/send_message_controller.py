import requests

def send_message(message, API_KEY, API_BASE_URL, session_id=None, chat_id=None):
    headers = {
        "X-API-Key": API_KEY
    }
    payload = {
        "chatId": chat_id,
        "text": message
    }
    if session_id is None or chat_id is None:
        return None
    
    response = requests.post(f"{API_BASE_URL}/api/sessions/{session_id}/messages/send-text", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None
