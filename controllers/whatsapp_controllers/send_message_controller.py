import requests

def send_message(phone_number, message, API_KEY, API_BASE_URL, session_id=None):
    headers = {
        "X-API-Key": API_KEY
    }
    payload = {
        "sessionId": session_id,
        "phone": phone_number,
        "message": message
    }
    response = requests.post(f"{API_BASE_URL}/api/send-message", headers=headers, json=payload)
    return response.json()