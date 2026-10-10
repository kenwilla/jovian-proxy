from detectors.email import EmailDetector
from detectors.credit_card import CreditCardDetector
from detectors.infrastructure import InfrastructureLeakDetector # 🌟 Added

# Make it plug-and-play so the engine can load them uniformly
ALL_DEFAULT_DETECTORS = [
    EmailDetector(), 
    CreditCardDetector(), 
    InfrastructureLeakDetector() # 🌟 Added!
]
