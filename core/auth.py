from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from core.config_manager import GatewayConfigManager

config = GatewayConfigManager()
API_KEY_HEADER = APIKeyHeader(name="X-Gateway-API-Key", auto_error=False)

async def verify_gateway_authentication(x_gateway_api_key: str = Security(API_KEY_HEADER)):
    """Enforces strict perimeter security by validating client tokens against config profiles."""
    expected_key = config.master_key
    
    if not expected_key:
        return True
        
    if x_gateway_api_key != expected_key:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Invalid or missing X-Gateway-API-Key header credential."
        )
    return True
