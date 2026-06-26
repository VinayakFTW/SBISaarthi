import requests

def get_wa_session_id(API_BASE_URL, API_KEY):
    headers = {
        "X-API-Key": API_KEY
    }

    if requests.get(f"{API_BASE_URL}/api/sessions", headers=headers).json()[0].get("name") == "sbi-saarthi":
        response = requests.get(f"{API_BASE_URL}/api/sessions", headers=headers).json()[0].get("id")
    else:
        payload = {
            "name": "sbi-saarthi",
            "config": {"autoreconnect": True,},
            "proxyUrl":API_BASE_URL,
            "proxyType": "http",
        }

        requests.post(f"{API_BASE_URL}/api/sessions", headers=headers, json=payload)
        response = requests.get(f"{API_BASE_URL}/api/sessions", headers=headers).json()[0].get("id")

    return response
