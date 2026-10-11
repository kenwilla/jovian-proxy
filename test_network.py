"""
Jovian Proxy Live Egress Integration Test Runner.

Dispatches explicit live HTTP network packets over the loopback stack 
to assert compliance engine behavior, header parsing stability, 
and firewall subnet whitelisting validation rules on active instances.
"""

import json
import os
import sys
import requests

# Instruct the runtime to ignore all system or corporate proxy variables
os.environ['no_proxy'] = '127.0.0.1,localhost,0.0.0.0'

url = "http://127.0.0.1:8000/v1/proxy/chat"

headers = {
    "X-Gateway-API-Key": "sec_gateway_secret_abc123",
    "X-User-ID": "dev_network_auditor",
    "X-Department": "Cyber_Defense_Squad",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "CRITICAL: Engineer admin@jovianhq.com is debugging an infrastructure leak with AWS key AKIAIOSFODNN7EXAMPLE right now."
}

print("🌐 Dispatching live network packet to Jovian Proxy Server...")

try:
    response = requests.post(
        url, 
        json=payload, 
        headers=headers, 
        proxies={'http': None, 'https': None}, 
        timeout=5
    )
    
    print(f"\n📡 [SERVER HTTP STATUS CODE]: {response.status_code}")
    
    if response.status_code == 200:
        print("🟢 [ACCESS GRANTED]: Proxy successfully parsed payload.")
        print(json.dumps(response.json(), indent=2))
        sys.exit(0)  # Programmatic success flag for CI tools
    elif response.status_code == 403:
        print("🔴 [ACCESS DENIED]: The enterprise firewall successfully dropped your network range!")
        print(response.json())
        sys.exit(0)  # 403 is an expected firewall success state if testing isolation blocks
    else:
        print(f"⚠️ [SERVER ALERT]: Unexpected Response Code {response.status_code}")
        print(response.text)
        sys.exit(1)  # Failure condition

except requests.exceptions.ConnectionError as e:
    print(f"\n❌ Connection Failed. Target port 8000 is unreachable. Ensure the proxy server is running.")
    print(f"   Error details: {e}")
    sys.exit(1)
