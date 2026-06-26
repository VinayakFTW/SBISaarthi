import requests

def get_wa_session_chats(API_BASE_URL, API_KEY,session_id=None):
    headers = {
        "X-API-Key": API_KEY
    }

    if session_id:
        response = requests.get(f"{API_BASE_URL}/api/sessions/{session_id}/chats", headers=headers)
        if response.status_code == 200:
            result = []
            for obj in response.json():
                chat_id = obj.get("id")
                chat_name = obj.get("name")
                result.append({"chat_id": chat_id, "chat_name": chat_name})
            return result
        else:
            return None
    else:
        return None
