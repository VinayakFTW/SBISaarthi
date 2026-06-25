import re

class DataMasker:
    # Aadhaar format: 12 digits, optional spaces or dashes
    AADHAAR_REGEX = r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b'
    # PAN format: 5 uppercase letters, 4 digits, 1 uppercase letter
    PAN_REGEX = r'\b[A-Z]{5}\d{4}[A-Z]{1}\b'

    @classmethod
    def mask(cls, text: str) -> str:
        if not text:
            return text
        masked_text = re.sub(cls.AADHAAR_REGEX, 'XXXX-XXXX-XXXX', text)
        masked_text = re.sub(cls.PAN_REGEX, 'XXXXX9999X', masked_text)
        return masked_text
