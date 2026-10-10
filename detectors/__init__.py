from core.config_manager import GatewayConfigManager  # Import settings manager
from detectors.email import EmailDetector
from detectors.credit_card import CreditCardDetector
from detectors.infrastructure import InfrastructureLeakDetector

def build_active_detector_suite() -> list:
    """Dynamically builds a list of active scanners matching the config profile."""
    config = GatewayConfigManager()
    active_suite = []
    
    if config.email_enabled:
        active_suite.append(EmailDetector())
        
    if config.credit_card_enabled:
        active_suite.append(CreditCardDetector())
        
    if config.infrastructure_enabled:
        active_suite.append(InfrastructureLeakDetector())
        
    return active_suite

ALL_DEFAULT_DETECTORS = build_active_detector_suite()
