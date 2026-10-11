from core.engine import GovernanceEngine
from core.config_manager import GatewayConfigManager  # 🌟 Updated Import
from detectors import build_active_detector_suite

# Initialize the manager explicitly right here
config_manager = GatewayConfigManager()

# Pass its validated setting cleanly into the engine constructor
engine = GovernanceEngine(
    detectors=build_active_detector_suite(), 
    ttl_seconds=config_manager.token_ttl
)
