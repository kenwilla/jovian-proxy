from core import engine

print("🛡️  Jovian Proxy Full-Spectrum Feature Flag Validation Test...")

# 🌟 A composite prompt containing ALL THREE leak types (Email, CC, AWS)
multi_leak_prompt = (
    "URGENT: Developer admin@jovianhq.com is debugging a deployment block. "
    "Check connection config using Visa card 4111-2222-3333-4444 "
    "and AWS Access Key ID AKIAIOSFODNN7EXAMPLE right away."
)

print("\n1. 🧑‍💻 [ORIGINAL PROMPT]:")
print(multi_leak_prompt)

# Execute the pipeline with explicit attribution strings
safe_prompt = engine.clean_outbound_prompt(
    text=multi_leak_prompt,
    user_id="dev_auditor_01",
    department="Security_Validation_Squad"
)

print("\n2. ☁️  [WHAT THE CLOUD AI SEES]:")
print(safe_prompt)
print("\n📊 Check your open web browser at http://127.0.0 to see the results render live!")
