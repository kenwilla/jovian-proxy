import ipaddress
import logging
from fastapi import HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from core.config_manager import config_manager

logger = logging.getLogger("jovian.auth")
API_KEY_HEADER = APIKeyHeader(name="X-Gateway-API-Key", auto_error=False)

# =====================================================================
# ⚡ HIGH-PERFORMANCE STATIC SUBNET CACHE
# =====================================================================
# Compile the network entities once during module initialization to guarantee O(1)-like fast execution speed
COMPILED_NETWORKS = []

if config_manager.whitelist_enabled:
    for network_entry in config_manager.allowed_networks:
        network_str = str(network_entry).strip()
        if not network_str:
            continue
        try:
            COMPILED_NETWORKS.append(ipaddress.ip_network(network_str, strict=False))
        except Exception as e:
            logger.error(f"❌ Failed to parse static subnet config boundary [{network_str}]: {e}")

async def verify_gateway_authentication(
    request: Request,
    x_gateway_api_key: str = Security(API_KEY_HEADER)
):
    # 🛡️ ENTERPRISE SECURITY: Subnet Range Firewall Execution
    if config_manager.whitelist_enabled:
        # Resolve real client IP even if sitting deep behind Nginx, Traefik, or AWS ALB layers
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            # Grab the leftmost original routing node in multi-hop proxy chains
            client_ip_str = x_forwarded_for.split(",")[0].strip()
        else:
            client_ip_str = request.client.host
        
        try:
            client_ip = ipaddress.ip_address(client_ip_str)
            access_granted = False
            
            # Evaluate against our highly efficient compiled cache
            for network in COMPILED_NETWORKS:
                if client_ip in network:
                    access_granted = True
                    break
                    
            if not access_granted:
                raise HTTPException(
                    status_code=403,
                    detail=f"Forbidden: Inbound network access denied for IP location: {client_ip_str}."
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: Network firewall validation failure: {str(e)}"
            )

    # 🔑 API KEY VALIDATION LAYER
    expected_key = config_manager.master_key
    if expected_key and x_gateway_api_key != expected_key:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Invalid or missing X-Gateway-API-Key header credential."
        )
        
    return True
