import yaml
import os

class GatewayConfigManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.settings = self._load_yaml_profile()

    def _load_yaml_profile(self) -> dict:
        default_settings = {
            "gateway": {"token_ttl_seconds": 600},
            "logging": {
                "log_directory": "logs",
                "log_filename_pattern": "{name}_{date}.jsonl",
                "log_base_name": "audit_log"
            },
            "chat_notifications": {
                "enabled": False,
                "provider": "slack",
                "webhook_url": "",
                "min_severity_level": "HIGH"
            }
        }
        
        if not os.path.exists(self.config_path):
            return default_settings
            
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded_yaml = yaml.safe_load(f)
                return loaded_yaml if loaded_yaml else default_settings
        except Exception:
            return default_settings

    @property
    def log_dir(self) -> str:
        return self.settings.get("logging", {}).get("log_directory", "logs")

    @property
    def log_pattern(self) -> str:
        return self.settings.get("logging", {}).get("log_filename_pattern", "{name}_{date}.jsonl")

    @property
    def log_base_name(self) -> str:
        return self.settings.get("logging", {}).get("log_base_name", "audit_log")

    @property
    def token_ttl(self) -> int:
        return self.settings.get("gateway", {}).get("token_ttl_seconds", 600)

    @property
    def master_key(self) -> str:
        return self.settings.get("security", {}).get("master_api_key", "")

    @property
    def email_enabled(self) -> bool:
        return self.settings.get("detectors", {}).get("email_scanner_enabled", True)

    @property
    def credit_card_enabled(self) -> bool:
        return self.settings.get("detectors", {}).get("credit_card_scanner_enabled", True)

    @property
    def infrastructure_enabled(self) -> bool:
        return self.settings.get("detectors", {}).get("infrastructure_scanner_enabled", True)
        
    @property
    def whitelist_enabled(self) -> bool:
        return self.settings.get("network", {}).get("ip_whitelist_enabled", False)

    @property
    def allowed_networks(self) -> list:
        return self.settings.get("network", {}).get("allowed_ip_networks", [])
        
    @property
    def webhook_enabled(self) -> bool:
        return self.settings.get("webhooks", {}).get("webhook_streaming_enabled", False)

    @property
    def webhook_url(self) -> str:
        return self.settings.get("webhooks", {}).get("target_destination_url", "")

    @property
    def chat_notifications(self) -> dict:
        """Returns the structural dictionary mapping for corporate Slack/Teams alerting pipelines."""
        return self.settings.get("chat_notifications", {
            "enabled": False,
            "provider": "slack",
            "webhook_url": "",
            "min_severity_level": "HIGH"
        })

config_manager = GatewayConfigManager()
