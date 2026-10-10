from core.engine import GovernanceEngine
from core.config_manager import GatewayConfigManager  # 🌟 Updated Import
from detectors import ALL_DEFAULT_DETECTORS

# Initialize the manager explicitly right here
config_manager = GatewayConfigManager()

# Pass its validated setting cleanly into the engine constructor
engine = GovernanceEngine(
    detectors=ALL_DEFAULT_DETECTORS, 
    ttl_seconds=config_manager.token_ttl
)
