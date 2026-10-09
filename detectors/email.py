import re
from typing import List, Dict
from detectors.base import BaseDetector

class EmailDetector(BaseDetector):
    """Detects and isolates email addresses using fast regex."""
    def __init__(self):
        super().__init__(name="RegexEmailDetector", entity_type="EMAIL")
        self.regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    def detect(self, text: str) -> List[Dict]:
        return [
            {"type": self.entity_type, "start": m.start(), "end": m.end(), "value": m.group()}
            for m in self.regex.finditer(text)
        ]
