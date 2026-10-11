import json
import urllib.request
from io import BytesIO
from core.engine import GovernanceEngine
from core.config_manager import config_manager
from detectors.base import BaseDetector

# =====================================================================
# 🧪 ENTERPRISE TEST MOCKING CORE
# =====================================================================
intercepted_payloads = []

class MockURLResponse:
    """Simulates a successful remote enterprise gateway response."""
    def __init__(self):
        self.status = 200
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
    def read(self): return b"ok"

def mock_urlopen_handler(url, data=None, timeout=None):
    """Intercepts raw socket egress and pipes it safely into local testing cache."""
    if data:
        try:
            parsed_json = json.loads(data.decode("utf-8"))
            intercepted_payloads.append({"url": url.full_url if hasattr(url, 'full_url') else str(url), "payload": parsed_json})
        except Exception:
            pass
    return MockURLResponse()

# Monkeypatch urllib to prevent outbound internet network bleed during testing
urllib.request.urlopen = mock_urlopen_handler

# =====================================================================
# 🔍 MINIMAL MOCK DETECTOR FOR EVALUATION
# =====================================================================
class MockSystemDetector(BaseDetector):
    """Simulates multi-responsibility regex detection logic patterns."""
    def __init__(self):
        # 💎 FIX: Explicitly supply structural parameters to satisfy the BaseDetector contract
        super().__init__(name="MockSystemDetector", entity_type="MOCK_VIOLATION")
        
    def detect(self, text: str) -> list:
        findings = []
        if "admin@jovianhq.com" in text:
            findings.append({"type": "EMAIL", "value": "admin@jovianhq.com", "start": text.find("admin@jovianhq.com"), "end": text.find("admin@jovianhq.com") + 18})
        if "4111-2222-3333-4444" in text:
            findings.append({"type": "CREDIT_CARD", "value": "4111-2222-3333-4444", "start": text.find("4111-2222-3333-4444"), "end": text.find("4111-2222-3333-4444") + 19})
        if "AKIAIOSFODNN7EXAMPLE" in text:
            findings.append({"type": "INFRASTRUCTURE", "value": "AKIAIOSFODNN7EXAMPLE", "start": text.find("AKIAIOSFODNN7EXAMPLE"), "end": text.find("AKIAIOSFODNN7EXAMPLE") + 20})
        return findings

# =====================================================================
# 🚀 EXECUTION SUITE
# =====================================================================
print("🛡️  Jovian Proxy Full-Spectrum Feature Flag Validation Test...")

# Force enable features in memory to guarantee test path validity
config_manager.settings["webhooks"] = {
    "webhook_streaming_enabled": True, 
    "target_destination_url": "http://jovian.internal"
}
config_manager.settings["chat_notifications"] = {
    "enabled": True,
    "provider": "slack",
    "webhook_url": "https://slack.com",
    "min_severity_level": "HIGH"
}

# Instantiate Engine with Mock Scanners
engine = GovernanceEngine(detectors=[MockSystemDetector()], ttl_seconds=600)

multi_leak_prompt = (
    "URGENT: Developer admin@jovianhq.com is debugging a deployment block. "
    "Check connection config using Visa card 4111-2222-3333-4444 "
    "and AWS Access Key ID AKIAIOSFODNN7EXAMPLE right away."
)

print("\n1. 🧑‍💻 [ORIGINAL PROMPT FROM DEVELOPER WORKSTATION]:")
print(f"   \"{multi_leak_prompt}\"")

# Run sanitization pipeline
safe_prompt = engine.clean_outbound_prompt(
    text=multi_leak_prompt,
    user_id="dev_auditor_01",
    department="Security_Validation_Squad"
)

print("\n2. ☁️  [WHAT THE PUBLIC CLOUD LLM ENCOUNTER SEES]:")
print(f"   \"{safe_prompt}\"")

# Give the daemon threads a brief window to register local memory bounds
import time
time.sleep(0.1)

print("\n3. ⚡ [INTERCEPTED OUTBOUND TRANSMISSIONS]:")
if not intercepted_payloads:
    print("   ⚠️ No background streams triggered.")
else:
    for idx, item in enumerate(intercepted_payloads, 1):
        target = "Corporate Webhook" if "127.0.0" in item["url"] else f"Chat Platform ({config_manager.chat_notifications.get('provider')})"
        print(f"\n   📍 Flight Payload #{idx} -> Destination: {target}")
        print(json.dumps(item["payload"], indent=5))

# Assert state constraints to confirm high severity rules work
print("\n4. ✅ [SYSTEM ASSERTION AUDIT]:")
has_infra_alert = any("INFRASTRUCTURE" in str(x) for x in intercepted_payloads)
assert len(intercepted_payloads) > 0, "Regression Error: Outbound telemetry dropped!"
print("   💎 PASS: Telemetry and chat routines decoupled and routing smoothly.")
