import requests

def typing_indicator(phone_number, API_KEY, API_BASE_URL, session_id=None,chat_id=None):
    headers = {
        "X-API-Key": API_KEY
    }
    payload = {
        "sessionId": chat_id,
        "state": "typing"
    }
    if not session_id or not chat_id:
        return {"error": "Session ID and Chat ID are required to send typing indicator."}
    
    response = requests.post(f"{API_BASE_URL}/api/sessions/{session_id}/chats/typing", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to send typing indicator. Status code: {response.status_code}, Response: {response.text}"}
