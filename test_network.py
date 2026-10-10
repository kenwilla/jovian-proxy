import requests
import json
import os

# Instruct the runtime to ignore all system or corporate proxy variables
os.environ['no_proxy'] = '127.0.0.1,localhost,0.0.0.0'

# Pristine, four-digit IP network endpoint tracking destination
url = "http://127.0.0.1:8000/v1/proxy/chat"

headers = {
    "X-Gateway-API-Key": "sec_gateway_secret_abc123",
    "X-User-ID": "dev_network_auditor",
    "X-Department": "Cyber_Defense_Squad",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "Testing live enterprise network transmission bounds."
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
    elif response.status_code == 403:
        print("🔴 [ACCESS DENIED]: The enterprise firewall successfully dropped your network range!")
        print(response.json())
    else:
        print(f"⚠️ [SERVER ALERT]: Code {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError as e:
    print(f"\n❌ Connection Failed. Network stack is blocked. Error details: {e}")
