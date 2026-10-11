import json
import os
from datetime import datetime, timezone
from core.config_manager import config_manager
from core.streamer import webhook_streamer

class JSONComplianceLogger:
    def __init__(self):
        pass

    def get_active_rotated_filepath(self) -> str:
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        target_directory = config_manager.log_dir
        pattern_layout = config_manager.log_pattern
        base_name = config_manager.log_base_name
        
        filename = pattern_layout.format(name=base_name, date=current_date)
        final_path = os.path.join(target_directory, filename)
        
        if target_directory and not os.path.exists(target_directory):
            os.makedirs(target_directory, exist_ok=True)
            
        return final_path

    def write_record(self, user_id: str, department: str, token_placeholder: str, entity_type: str):
        now = datetime.now(timezone.utc)
        timestamp_iso = now.isoformat()
        
        log_record = {
            "timestamp_utc": timestamp_iso,
            "attribution": {"user_id": user_id, "department": department},
            "security_event": {
                "token_placeholder": token_placeholder,
                "detected_entity_type": entity_type,
                "action_taken": "ANONYMIZED_AND_VAULTED"
            }
        }
        
        active_file_path = self.get_active_rotated_filepath()
        
        with open(active_file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(log_record) + "\n")
        
        webhook_streamer.stream_event_payload(
            user_id=user_id,
            department=department,
            token_placeholder=token_placeholder,
            entity_type=entity_type,
            timestamp_iso=timestamp_iso
        )
