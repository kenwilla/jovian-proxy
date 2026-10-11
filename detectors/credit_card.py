import re
from typing import List, Dict
from detectors.base import BaseDetector

class CreditCardDetector(BaseDetector):
    """
    Perimeter scanner optimizing linear regular expressions to capture financial card strings.
    
    Designed to process Luhn-range numeric fields with zero risk of catastrophic backtracking.
    """
    def __init__(self):
        super().__init__(name="RegexCCDetector", entity_type="CREDIT_CARD")
        # Matches 13 to 16 digit number strings securely separated by standard spaces or dashes
        self.regex = re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{1,4}\b|\b\d{13,16}\b')

    def detect(self, text: str) -> List[Dict]:
        return [
            {
                "type": self.entity_type, 
                "start": m.start(), 
                "end": m.end(), 
                "value": m.group()
            }
            for m in self.regex.finditer(text)
        ]
