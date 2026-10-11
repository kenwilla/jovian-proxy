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

    def _execute_chat_alert(self, provider: str, webhook_url: str, log_record: dict):
        """Dispatches structured, visually deep cards natively into enterprise chat spaces."""
        entity_type = log_record["security_event"]["detected_entity_type"]
        user_id = log_record["attribution"]["user_id"]
        dept = log_record["attribution"]["department"]
        timestamp = log_record["timestamp_utc"]
        
        chat_payload = {}
        
        if provider == "slack":
            chat_payload = {
                "text": f"🚨 Jovian Proxy Leak Prevented: {entity_type}",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🚨 HIGH SEVERITY: Security Leak Shielded",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Detector Triggered:*\n`{entity_type}`"},
                            {"type": "mrkdwn", "text": f"*User Attribution:*\n`{user_id} ({dept})`"},
                            {"type": "mrkdwn", "text": f"*Action Implemented:*\n`Stateful Tokenization`"},
                            {"type": "mrkdwn", "text": f"*Timestamp UTC:*\n`{timestamp}`"}
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            {"type": "mrkdwn", "text": "🛡️ *Jovian Proxy Perimeter Controls* • Infrastructure Leak Protection Suite"}
                        ]
                    }
                ]
            }
        elif provider == "teams":
            chat_payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org",
                "themeColor": "FF0000",
                "summary": f"Jovian Proxy Security Threat Blocked: {entity_type}",
                "sections": [{
                    "activityTitle": "🛡️ Jovian Proxy Perimeter Protection Alert",
                    "activitySubtitle": "Severity Level: **CRITICAL (High-Risk Leak)**",
                    "facts": [
                        {"name": "Triggered Scanner", "value": entity_type},
                        {"name": "Attributed User", "value": f"{user_id} ({dept})"},
                        {"name": "Mitigation Strategy", "value": "Volatile RAM Stateful Masking"}
                    ],
                    "markdown": True
                }]
            }
        else:
            return

        try:
            data_bytes = json.dumps(chat_payload).encode("utf-8")
            req = urllib.request.Request(
                webhook_url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=4) as _:
                pass
        except Exception as e:
            print(f"⚠️  [JOVIAN CHAT WORKER]: Failed to ship {provider} alert over the wire: {e}")

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
        
        chat_cfg = getattr(config_manager, "chat_notifications", {})
        if chat_cfg and chat_cfg.get("enabled", False):
            min_severity = chat_cfg.get("min_severity_level", "HIGH")
            
            if min_severity == "HIGH" and "infrastructure" not in entity_type.lower():
                return
                
            provider = chat_cfg.get("provider", "slack").lower()
            webhook_url = chat_cfg.get("webhook_url")
            
            if webhook_url:
                threading.Thread(
                    target=self._execute_chat_alert, 
                    args=(provider, webhook_url, log_record), 
                    daemon=True
                ).start()

webhook_streamer = BackgroundWebhookStreamer()
