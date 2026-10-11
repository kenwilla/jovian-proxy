"""
Jovian Proxy Detector Integration Workspace.

Provides centralized management and dynamic instantiation contracts for individual regular 
expression and string analysis scanning layers using a lazy factory allocation model.
"""

from core.config_manager import config_manager
from detectors.email import EmailDetector
from detectors.credit_card import CreditCardDetector
from detectors.infrastructure import InfrastructureLeakDetector

def build_active_detector_suite() -> list:
    """
    Dynamically builds and allocates active scanner objects based on configuration profile states.

    Returns:
        list: An active collection of instantiated BaseDetector subclasses ready for parsing.
    """
    active_suite = []
    
    if config_manager.email_enabled:
        active_suite.append(EmailDetector())
        
    if config_manager.credit_card_enabled:
        active_suite.append(CreditCardDetector())
        
    if config_manager.infrastructure_enabled:
        active_suite.append(InfrastructureLeakDetector())
        
    return active_suite
