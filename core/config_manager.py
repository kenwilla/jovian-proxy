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
                # Graceful backup step if the YAML file is empty
                return loaded_yaml if loaded_yaml else default_settings
        except Exception:
            return default_settings

    @property
    def token_ttl(self) -> int:
        return self.settings.get("gateway", {}).get("token_ttl_seconds", 600)

    @property
    def log_path(self) -> str:
        return self.settings.get("logging", {}).get("log_file_path", "audit_log.jsonl")

# Instantiated globally for single-responsibility state lookup across modules
config_manager = GatewayConfigManager()
