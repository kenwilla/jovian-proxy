from core import engine

# Simulate a contractor on the offshore development squad trying to leak credentials
mock_prompt = "Pasting the production password file for dev-lead@offshore-vendor.com right now."
print("🚀 Simulating active context-aware text flow...")

# Execute the pipeline with explicit attribution strings passed directly
safe_prompt = engine.clean_outbound_prompt(
    text=mock_prompt,
    user_id="emp_contractor_402",
    department="Offshore_Engineering_Group"
)

print("\n✨ Clean text engineered successfully.")
print("📊 Inspecting audit_log.csv for contextual records...")
