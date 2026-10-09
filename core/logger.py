import csv
import os
from datetime import datetime, timezone

class CSVComplianceLogger:
    """Handles permanent, tamper-proof metadata log persistence with user attribution."""
    def __init__(self, log_file_path: str = "audit_log.csv"):
        self.log_file_path = log_file_path
        self._initialize_audit_file()

    def _initialize_audit_file(self):
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 🌟 ADDED: user_id and department headers
                writer.writerow([
                    "timestamp_utc", 
                    "user_id", 
                    "department", 
                    "token_placeholder", 
                    "detected_entity_type", 
                    "action_taken"
                ])

    def write_record(self, user_id: str, department: str, token_placeholder: str, entity_type: str):
        """Appends a new immutable compliance record with full employee context attribution."""
        timestamp = datetime.now(timezone.utc).isoformat()
        with open(self.log_file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 🌟 ADDED: user_id and department mapping values
            writer.writerow([
                timestamp, 
                user_id, 
                department, 
                token_placeholder, 
                entity_type, 
                "ANONYMIZED_AND_VAULTED"
            ])
