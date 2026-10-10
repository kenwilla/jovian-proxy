import ipaddress
from fastapi import HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from core.config_manager import config_manager

API_KEY_HEADER = APIKeyHeader(name="X-Gateway-API-Key", auto_error=False)

async def verify_gateway_authentication(
    request: Request,
    x_gateway_api_key: str = Security(API_KEY_HEADER)
):
    # 🛡️ ENTERPRISE SECURITY: CIDR Subnet Range Network Validation
    if config_manager.whitelist_enabled:
        client_ip_str = request.client.host
        
        try:
            # Parse raw text address string into a secure Python IP Object
            client_ip = ipaddress.ip_address(client_ip_str)
            access_granted = False
            
            # Mathematically test if the client lives inside any corporate subnets
            for network_entry in config_manager.allowed_networks:
                # Force entry validation to an explicit text string layout
                network_str = str(network_entry).strip()
                if not network_str:
                    continue
                    
                network = ipaddress.ip_network(network_str, strict=False)
                if client_ip in network:
                    access_granted = True
                    break
                    
            if not access_granted:
                raise HTTPException(
                    status_code=403,
                    detail=f"Forbidden: Inbound network access denied for IP address location {client_ip_str}."
                )
        except HTTPException:
            raise  # Re-raise our own 403 blocks cleanly
        except Exception as e:
            # Catch and report formatting issues that trigger 500 errors
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: Network firewall syntax execution error: {str(e)}"
            )

    # 🔑 API KEY VALIDATION LAYER
    expected_key = config_manager.master_key
    if expected_key and x_gateway_api_key != expected_key:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Invalid or missing X-Gateway-API-Key header credential."
        )
        
    return True
