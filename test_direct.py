from core import engine

print("🚀 Executing deep structural JSON security scan...")

# Simulate an offshore developer pushing a prompt with nested PII violations
engine.clean_outbound_prompt(
    text="URGENT: Run test compile for john.doe@offshore-vendor.com using Visa card 4111-2222-3333-4444.",
    user_id="dev_offshore_992",
    department="Contract_Vendor_Squad"
)

print("✨ Security logs engineered.")
print("📊 Opening audit_log.jsonl payload map...\n")

# Read the newly created JSON lines file locally to verify structure
with open("audit_log.jsonl", "r") as log_file:
    for line in log_file:
        print(line.strip())
