from fastapi import APIRouter, Request
from app.services.proxy import forward_request
from app.core.limiter import limiter

router = APIRouter()

@router.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@limiter.limit("100/minute")
async def gateway_proxy(request: Request, service_name: str, path: str):
    return await forward_request(service_name, path, request)