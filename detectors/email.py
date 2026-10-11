import re
from typing import List, Dict
from detectors.base import BaseDetector

class EmailDetector(BaseDetector):
    """
    High-throughput corporate email regex engine.
    
    Extracts structured routing targets safely across complex development content streams.
    """
    def __init__(self):
        super().__init__(name="RegexEmailDetector", entity_type="EMAIL")
        # Hardened parsing format targeting standard RFC-compliant electronic mail coordinates
        self.regex = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')

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
