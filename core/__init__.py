from core.engine import GovernanceEngine
from detectors import ALL_DEFAULT_DETECTORS

# Initialize the global core engine instance out of the box
engine = GovernanceEngine(detectors=ALL_DEFAULT_DETECTORS, ttl_seconds=600)
