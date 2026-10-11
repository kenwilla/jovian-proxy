import re
from typing import List, Dict
from detectors.base import BaseDetector

class InfrastructureLeakDetector(BaseDetector):
    """
    Cloud platform authorization scanner.
    
    Intercepts dynamic credential strings, cloud authentication tokens, and infrastructure keys.
    """
    def __init__(self):
        super().__init__(name="InfrastructureLeakDetector", entity_type="CLOUD_CREDENTIAL")
        self.aws_regex = re.compile(r'\bAKIA[A-Z0-9]{16}\b')
        self.bearer_regex = re.compile(r'\bBearer\s+[a-zA-Z0-9_\-\.]+\b', re.IGNORECASE)

    def detect(self, text: str) -> List[Dict]:
        results = []
        
        # Scan for AWS Identity Keys
        for m in self.aws_regex.finditer(text):
            results.append({
                "type": self.entity_type, 
                "start": m.start(), 
                "end": m.end(), 
                "value": m.group()
            })
            
        # Scan for Bearer Tokens (captures the full prefix string to shield context boundaries)
        for m in self.bearer_regex.finditer(text):
            results.append({
                "type": self.entity_type, 
                "start": m.start(), 
                "end": m.end(), 
                "value": m.group()
            })
            
        return results
