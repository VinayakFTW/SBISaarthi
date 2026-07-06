# utils/openwa_helpers.py

import os
import httpx

OPENWA_URL = os.getenv("OPENWA_URL")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY")

async def resolve_chat_id_to_phone(session_id: str, chat_id: str) -> str:
    """
    Translates a WhatsApp @lid to a raw phone number asynchronously.
    Returns the resolved number, or None if it fails.
    """
    if not session_id or not chat_id:
        return None

    headers = {"X-API-Key": OPENWA_API_KEY}
    url = f"{OPENWA_URL}/api/sessions/{session_id}/contacts/{chat_id}/phone"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=5.0)
            if response.status_code == 200:
                phone = response.json().get("phone")
                if phone and phone.isnumeric():
                    return phone
        except Exception as e:
            print(f"Failed to resolve LID to phone: {str(e)}")
            
    return None