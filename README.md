# Jovian Proxy 🛡️

An open-core, ultra-low latency data anonymization and stateful tokenization gateway shield designed for modern enterprise ecosystems. Jovian Proxy sits as a perimeter defense layer, absorbing high-risk PII strings, financial records, and infrastructure credential leaks before your data ever exits the corporate perimeter to public cloud AI endpoints.

Named in tribute to the Jovian cosmic shields that intercept and absorb rogue impacts to protect the space within.

## Core Architecture
- **Zero-Trust Tokenization Suite:** Intercepts outbound prompts or file streams and masks high-risk strings utilizing modular scanners.
- **Stateful Inbound Reversal Vault:** Registers temporary tokens to volatile system memory, allowing downstream AI responses to map context cleanly and natively back to internal work environments.
- **Automated Memory Expiry Execution (TTL Cache):** Tokens actively self-destruct from system RAM based on configurable expiration windows to guarantee strict security compliance.
- **Structured JSONL Logger:** Records metadata compliance metrics line-by-line via streaming JSON Lines (`.jsonl`) without logging underlying sensitive text—frontend-ready and optimized for SIEM systems like Splunk or Datadog.
- **Perimeter Authentication:** Enforces secure integration boundaries by validating client queries against external `config.yaml` token settings.
- **Decoupled Feature Flags:** Allows administrators to dynamically toggle individual detector pipelines on or off at runtime via a centralized settings file without touching core application logic.
- **Incident Escalation Engine:** Streams rich, asynchronous layout cards straight into collaborative workspace channels when critical leaks occur.

## Project Structure
```text
├── core/            # Gateway orchestration, validation filters, loggers, and streamers
├── detectors/       # Modular, single-responsibility regex & NLP scanners
├── main.py          # Asynchronous FastAPI route gateway handlers
└── test_direct.py   # Isolated mock evaluation pipeline tool
```

## Configuration Matrix (`config.yaml`)
You can fully decouple settings from logic using the centralized profile file:
```yaml
gateway:
  token_ttl_seconds: 600

logging:
  log_directory: "logs"
  log_filename_pattern: "{name}_{date}.jsonl"
  log_base_name: "audit_log"

security:
  master_api_key: "sec_gateway_secret_abc123"

detectors:
  email_scanner_enabled: true
  credit_card_scanner_enabled: true
  infrastructure_scanner_enabled: true

chat_notifications:
  enabled: true
  provider: "slack" # Options: "slack" or "teams"
  webhook_url: "https://slack.com..."
  min_severity_level: "HIGH" # Filter options: "ALL" or "HIGH" (infrastructure only)
```

### Logging Variable Templates
The `log_filename_pattern` parameter supports dynamic pattern mapping tokens inside `config.yaml` to ensure clean integration with downstream corporate data pipelines:

| Placeholder | Replaced Value | Example Output Transformation |
| :--- | :--- | :--- |
| `{name}` | Substitutes the exact string defined inside the `log_base_name` field. | `audit_log` |
| `{date}` | Appends the current calendar stamp automatically using the `YYYY-MM-DD` format. | `2026-10-11` |

### Chat Notification Providers
The alerting engine maps internal events directly into complex interface templates unique to each provider profile:

* **`slack`**: Fires a rich **Slack Block Kit** layout containing formatted section blocks, metadata tracking columns, and colored system indicators.
* **`teams`**: Formats an **Office 365 Connector MessageCard** schema featuring Markdown-rendered factual lists and targeted warning outlines.

## Getting Started
1. Clone the repository and install requirements:
   ```bash
   pip install fastapi uvicorn pydantic requests PyYAML
   ```
2. Execute the full-spectrum verification suite:
   ```bash
   python test_direct.py
   ```

## License
Licensed under the GNU Affero General Public License v3 (**AGPLv3**). See LICENSE for details. Developed for enterprise data security applications.
