import re
from typing import List, Dict
from detectors.base import BaseDetector

class InfrastructureLeakDetector(BaseDetector):
    """Detects leaked cloud infrastructure credentials like AWS Access Keys and Bearer Tokens."""
    def __init__(self):
        super().__init__(name="InfrastructureLeakDetector", entity_type="CLOUD_CREDENTIAL")
        # Matches standard AWS Access Key structures (AKIA followed by 16 alphanumeric characters)
        self.aws_regex = re.compile(r'\b(AKIA[A-Z0-9]{16})\b')
        # Matches standard authorization Bearer token headers
        self.bearer_regex = re.compile(r'Bearer\s+([a-zA-Z0-9_\-\.]+)', re.IGNORECASE)

    def detect(self, text: str) -> List[Dict]:
        results = []
        
        # Scan for AWS Access Keys
        for m in self.aws_regex.finditer(text):
            results.append({"type": self.entity_type, "start": m.start(1), "end": m.end(1), "value": m.group(1)})
            
        # Scan for Bearer Tokens
        for m in self.bearer_regex.finditer(text):
            results.append({"type": self.entity_type, "start": m.start(1), "end": m.end(1), "value": m.group(1)})
            
        return results
