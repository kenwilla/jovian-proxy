# Secure AI Governance Gateway Proxy 🛡️

An open-core, ultra-low latency data anonymization and stateful tokenization gateway engine designed for modern enterprises. Protects proprietary data pipelines from leaking into public cloud AI endpoints (OpenAI, Anthropic, Claude) before data ever leaves your corporate perimeter.

## Core Pillars
- **Zero-Trust Tokenization Layer:** Intercepts outgoing chat prompts or file streams, parses data structure, and masks high-risk PII strings using modular scanners.
- **Stateful Inbound Reversal Vault:** Registers data tokens to local system memory, enabling the engine to map context seamlessly back to your internal developers while exposing 0% raw text to cloud logs.
- **Automated Memory Expiry Execution (TTL Cache):** Tokens actively self-destruct from volatile server RAM after 10 minutes to guarantee complete privacy compliance.
- **Zero Log Leakage Audit Trail:** Automatically writes structured event logs to a local CSV file tracking security incidents with millisecond precision without storing any underlying raw PII text.

## Project Structure
```text
├── core/            # Gateway orchestration, session tracking, and CSV loggers
├── detectors/       # Modular, single-responsibility regex & NLP detection classes
├── main.py          # Asynchronous FastAPI route gateway handlers
└── test_direct.py   # Isolated mock evaluation pipeline tool
```

## Getting Started

### Local Setup (No-Network Direct Engine Test)
1. Clone the repository and install requirements:
   ```bash
   pip install fastapi uvicorn pydantic requests
   ```
2. Execute the self-contained verification suite:
   ```bash
   python test_direct.py
   ```

## License
Licensed under the GNU Affero General Public License v3 (**AGPLv3**). See LICENSE for details. Developed for high-leverage data security applications.
