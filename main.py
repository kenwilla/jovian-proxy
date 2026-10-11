"""
Jovian Proxy Core Application Route Matrix.

Configures high-throughput, perimeter-defended FastAPI endpoints to intercept, 
anonymize, and stream metrics from outbound engineering prompts while exposing 
a secure visual monitoring analytics deck.
"""

import json
import os
from typing import Optional
from fastapi import FastAPI, Header, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core import engine
from core.auth import verify_gateway_authentication 
from core.config_manager import config_manager

app = FastAPI(title="Secure AI Gateway Proxy")

class ChatPayload(BaseModel): 
    prompt: str

class RestorePayload(BaseModel):
    text: str

@app.post("/v1/proxy/chat")
async def proxy_chat_endpoint(
    payload: ChatPayload,
    request: Request,
    x_user_id: Optional[str] = Header(default="UNKNOWN"),
    x_department: Optional[str] = Header(default="UNKNOWN"),
    _: bool = Depends(verify_gateway_authentication)
):
    """
    Intercepts outbound user traffic via HTTP headers and cleans sensitive data pools.
    """
    clean_text = engine.clean_outbound_prompt(
        text=payload.prompt, 
        user_id=x_user_id, 
        department=x_department
    )
    return {
        "status": "SECURED",
        "sanitized_prompt": clean_text
    }

@app.post("/v1/proxy/restore")
async def proxy_restore_endpoint(
    payload: RestorePayload,
    request: Request,
    _: bool = Depends(verify_gateway_authentication)
):
    """
    Intercepts inbound AI responses and restores masked tokens back to their original values.
    """
    try:
        restored_text = engine.restore_inbound_response(ai_response_text=payload.text)
        return {
            "status": "RESTORED",
            "restored_text": restored_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal State Reversal Fault: {str(e)}")

@app.get("/dashboard", response_class=HTMLResponse)
async def visual_analytics_dashboard(
    _: bool = Depends(verify_gateway_authentication)
):
    """
    Parses streaming log matrices from local storage to render an enterprise compliance grid view.
    """
    log_records = []
    log_path = engine.logger.get_active_rotated_filepath()
        
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        log_records.append(json.loads(line.strip()))
                    except Exception:
                        continue
                    
    log_records.reverse()
    
    table_rows = ""
    for log in log_records:
        table_rows += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; font-family: monospace;">{log.get('timestamp_utc', 'N/A')}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #4a5568;">{log.get('attribution', {}).get('user_id', 'UNKNOWN')}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #718096;">{log.get('attribution', {}).get('department', 'UNKNOWN')}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; font-family: monospace; background: #edf2f7; border-radius: 4px;">{log.get('security_event', {}).get('token_placeholder', 'N/A')}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;"><span style="background: #fed7d7; color: #9b2c2c; padding: 4px 8px; border-radius: 12px; font-size: 0.85em; font-weight: bold;">{log.get('security_event', {}).get('detected_entity_type', 'UNKNOWN')}</span></td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jovian Perimeter Control Center</title>
        <meta http-equiv="refresh" content="5"> <!-- Auto-refreshes security feed every 5 seconds -->
    </head>
    <body style="font-family: system-ui, sans-serif; background: #f7fafc; margin: 0; padding: 40px; color: #2d3748;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
                <div>
                    <h1 style="margin: 0; font-size: 2.2em; color: #1a202c;">🛡️ Jovian Proxy Perimeter Control Center</h1>
                    <p style="margin: 5px 0 0 0; color: #718096;">Real-Time Enterprise Compliance Stream Audit Ledger</p>
                </div>
                <div style="background: #3182ce; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 0.9em;">
                    🔒 PERIMETER KEY: ENFORCED
                </div>
            </div>
            
            <div style="background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                        <tr style="background: #ebf8ff; color: #2b6cb0; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.05em;">
                            <th style="padding: 16px;">Timestamp (UTC)</th>
                            <th style="padding: 16px;">User ID</th>
                            <th style="padding: 16px;">Department</th>
                            <th style="padding: 16px;">Traceable Token</th>
                            <th style="padding: 16px;">Violation Blocked</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows if table_rows else '<tr><td colspan="5" style="padding: 40px; text-align: center; color: #a0aec0;">No compliance violations logged yet. Gateway secure.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/v1/internal/collector", dependencies=[Depends(verify_gateway_authentication)])
async def mock_central_telemetry_collector(payload: dict):
    """
    Acts as a mock destination endpoint matching your future cloud platform dashboard.
    """
    print(f"\n📡 [CLOUD WEBHOOK INGESTED]: Event transmitted successfully!")
    print(json.dumps(payload, indent=2))
    return {"status": "RECEIVED"}
