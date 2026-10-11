import time
from typing import List, Dict
from detectors.base import BaseDetector
from core.logger import JSONComplianceLogger
from core.streamer import webhook_streamer

class GovernanceEngine:
    def __init__(self, detectors: List[BaseDetector], ttl_seconds: int = 600):
        self.detectors = detectors
        self.logger = JSONComplianceLogger()
        self.ttl_seconds = ttl_seconds
        self.vault: Dict[str, Dict] = {}

    def _evict_expired_tokens(self):
        """Cleans up system RAM by purging expired tokens from the memory vault."""
        current_time = time.time()
        expired_tokens = [
            token for token, data in self.vault.items() 
            if current_time > data["expires_at"]
        ]
        for token in expired_tokens:
            del self.vault[token]

    def clean_outbound_prompt(self, text: str, user_id: str = "UNKNOWN", department: str = "UNKNOWN") -> str:
        self._evict_expired_tokens()
        
        all_findings = []
        for detector in self.detectors:
            all_findings.extend(detector.detect(text))
        
        all_findings.sort(key=lambda x: x["start"], reverse=True)
        anonymized_text = text
        
        current_time = time.time()
        expiry_timestamp = current_time + self.ttl_seconds
        timestamp_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(current_time))
        
        for idx, finding in enumerate(all_findings):
            token_placeholder = f"USER_TOKEN_{finding['type']}_{idx+1}"
            real_value = finding['value']
            
            self.vault[token_placeholder] = {
                "value": real_value,
                "expires_at": expiry_timestamp
            }
            
            self.logger.write_record(user_id, department, token_placeholder, finding['type'])
            
            webhook_streamer.stream_event_payload(
                user_id=user_id,
                department=department,
                token_placeholder=token_placeholder,
                entity_type=finding['type'],
                timestamp_iso=timestamp_iso
            )
            
            anonymized_text = (
                anonymized_text[:finding["start"]] + 
                token_placeholder + 
                anonymized_text[finding["end"]:]
            )
            
        return anonymized_text

    def restore_inbound_response(self, ai_response_text: str) -> str:
        self._evict_expired_tokens()
        restored_text = ai_response_text
        
        for token_placeholder, data in self.vault.items():
            if token_placeholder in restored_text:
                restored_text = restored_text.replace(token_placeholder, data["value"])
        return restored_text
