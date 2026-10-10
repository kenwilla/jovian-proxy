import json
from datetime import datetime, timezone
from core.config_manager import config_manager # <--- Added configuration link

class JSONComplianceLogger:
    """Handles permanent, structured JSON log persistence powered by external settings."""
    def __init__(self):
        # 🌟 UPDATED: Dynamic lookup via config manager property
        self.log_file_path = config_manager.log_path

    def write_record(self, user_id: str, department: str, token_placeholder: str, entity_type: str):
        timestamp = datetime.now(timezone.utc).isoformat()
        
        log_record = {
            "timestamp_utc": timestamp,
            "attribution": {"user_id": user_id, "department": department},
            "security_event": {
                "token_placeholder": token_placeholder,
                "detected_entity_type": entity_type,
                "action_taken": "ANONYMIZED_AND_VAULTED"
            }
        }
        
        with open(self.log_file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(log_record) + "\n")
