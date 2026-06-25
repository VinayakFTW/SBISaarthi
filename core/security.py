import re
import uuid

class DataMasker:
    AADHAAR_REGEX = r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b'
    PAN_REGEX = r'\b[A-Z]{5}\d{4}[A-Z]{1}\b'
    
    vault = {}

    @classmethod
    def mask(cls, text: str) -> str:
        if not text:
            return text
            
        def replace_aadhaar(match):
            token = f"TOKEN_AADHAAR_{uuid.uuid4().hex[:8]}"
            cls.vault[token] = match.group(0)
            return token
            
        def replace_pan(match):
            token = f"TOKEN_PAN_{uuid.uuid4().hex[:8]}"
            cls.vault[token] = match.group(0)
            return token

        masked_text = re.sub(cls.AADHAAR_REGEX, replace_aadhaar, text)
        masked_text = re.sub(cls.PAN_REGEX, replace_pan, masked_text)
        return masked_text
        
    @classmethod
    def unmask(cls, text: str) -> str:
        if not text:
            return text
        unmasked = text
        for token, original in cls.vault.items():
            if token in unmasked:
                unmasked = unmasked.replace(token, original)
        return unmasked
