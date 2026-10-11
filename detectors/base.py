from typing import List, Dict

class BaseDetector:
    """
    Abstract Base Blueprint for all Jovian Proxy traffic scanners.
    
    Enforces contract uniformity to ensure that custom pattern-matching extensions 
    consistently return standardized index matrices to the primary orchestration engine.
    """
    def __init__(self, name: str, entity_type: str):
        self.name = name
        self.entity_type = entity_type

    def detect(self, text: str) -> List[Dict]:
        """
        Scans a text payload and returns a list of detected data entities.

        Args:
            text (str): The raw incoming text prompt or file stream slice.

        Returns:
            List[Dict]: An entry structure containing keys: 'type', 'start', 'end', 'value'.
        """
        raise NotImplementedError("Subclasses must implement the detect abstract contract pattern.")
