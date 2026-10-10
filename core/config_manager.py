import yaml
import os

class GatewayConfigManager:
    """Handles parsing, validation, and safe extraction of external configuration profiles."""
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.settings = self._load_yaml_profile()

    def _load_yaml_profile(self) -> dict:
        """Reads the local configuration file or returns hardcoded safe defaults if missing."""
        default_settings = {
            "gateway": {"token_ttl_seconds": 600},
            "logging": {"log_file_path": "audit_log.jsonl"}
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
    def token_ttl(self) -> int:
        return self.settings.get("gateway", {}).get("token_ttl_seconds", 600)

    @property
    def log_path(self) -> str:
        return self.settings.get("logging", {}).get("log_file_path", "audit_log.jsonl")
        
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

config_manager = GatewayConfigManager()
