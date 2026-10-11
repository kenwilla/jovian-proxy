import json
import urllib.request
import threading
from core.config_manager import config_manager

class BackgroundWebhookStreamer:
    def _execute_outbound_post(self, payload: dict):
        if not config_manager.webhook_enabled:
            return
        
        print(f"\n🚀 [JOVIAN WEBHOOK WORKER]: Outbound payload compiled. Shipping telemetry...")
        print(json.dumps(payload, indent=2))
        
        target_url = config_manager.webhook_url
        if not target_url:
            return
            
        try:
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                target_url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=3) as _:
                pass
        except Exception as e:
            print(f"⚠️  [JOVIAN WEBHOOK WORKER]: Local network request bypass condition handled: {e}")

    def stream_event_payload(self, user_id: str, department: str, token_placeholder: str, entity_type: str, timestamp_iso: str):
        log_record = {
            "timestamp_utc": timestamp_iso,
            "attribution": {"user_id": user_id, "department": department},
            "security_event": {
                "token_placeholder": token_placeholder,
                "detected_entity_type": entity_type,
                "action_taken": "ANONYMIZED_AND_VAULTED"
            }
        }
        threading.Thread(target=self._execute_outbound_post, args=(log_record,), daemon=True).start()

webhook_streamer = BackgroundWebhookStreamer()
