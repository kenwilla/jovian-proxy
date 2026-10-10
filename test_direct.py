from core import engine

print("🚀 Testing Jovian Proxy Cloud Infrastructure Leak Shield...")

# Simulate an offshore engineer pasting an error log containing an AWS key
mock_prompt = "Error: Connection failed for AWS key AKIAIOSFODNN7EXAMPLE using Bearer secret-token-12345."

safe_prompt = engine.clean_outbound_prompt(
    text=mock_prompt,
    user_id="dev_offshore_302",
    department="Cloud_Infrastructure_Group"
)

print("\n☁️ [WHAT THE CLOUD AI SEES]:")
print(safe_prompt)

print("\n📊 Check your open web browser at http://127.0.0 to see it live!")
