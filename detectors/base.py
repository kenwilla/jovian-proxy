from typing import List, Dict

class BaseDetector:
    """The strict blueprint that all future detectors must follow."""
    def __init__(self, name: str, entity_type: str):
        self.name = name
        self.entity_type = entity_type

    def detect(self, text: str) -> List[Dict]:
        raise NotImplementedError
