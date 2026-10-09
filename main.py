from fastapi import FastAPI
from pydantic import BaseModel
from core import engine

app = FastAPI(title="Secure AI Gateway Proxy")

class ChatPayload(BaseModel):
    prompt: str

@app.post("/v1/proxy/chat")
async def proxy_chat_endpoint(
    payload: ChatPayload,
    # 🌟 FastAPI reads these custom corporate network headers out of the request dynamically
    x_user_id: Optional[str] = Header(default="UNKNOWN"),
    x_department: Optional[str] = Header(default="UNKNOWN")
):
    # Pass them directly down into the governance core execution track
    clean_text = engine.clean_outbound_prompt(
        text=payload.prompt, 
        user_id=x_user_id, 
        department=x_department
    )
    return {
        "status": "SECURED",
        "sanitized_prompt": clean_text
    }
