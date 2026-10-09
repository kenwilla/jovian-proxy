import re
from typing import List, Dict
from detectors.base import BaseDetector

class CreditCardDetector(BaseDetector):
    """Detects generic 16-digit credit card sequences."""
    def __init__(self):
        super().__init__(name="RegexCCDetector", entity_type="CREDIT_CARD")
        self.regex = re.compile(r'\b(?:\d[ -]*?){13,16}\b')

    def detect(self, text: str) -> List[Dict]:
        return [
            {"type": self.entity_type, "start": m.start(), "end": m.end(), "value": m.group()}
            for m in self.regex.finditer(text)
        ]
