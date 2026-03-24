import httpx
from fastapi import Request, Response, HTTPException
from app.core.config import SERVICES_MAP
from app.core.security import verify_gateway_token

async def forward_request(service_name: str, path: str, request: Request) -> Response:
    if service_name not in SERVICES_MAP:
        raise HTTPException(status_code=404, detail="Servicio no registrado.")

    base_url = SERVICES_MAP[service_name].rstrip("/")
    target_url = f"{base_url}/{service_name}/{path}" 
    
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    # 🛡️ SEGURIDAD: Traducción de Cookie a Header para el Chatbot
    if service_name == "chat":
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Falta cookie de acceso.")
        
        clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
        verify_gateway_token(clean_token)
        headers["Authorization"] = f"Bearer {clean_token}"

    timeout = httpx.Timeout(120.0) 
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            proxy_req = client.build_request(
                method=request.method, url=target_url, headers=headers,
                content=body, params=request.query_params, cookies=request.cookies
            )
            proxy_res = await client.send(proxy_req)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Servicio no disponible: {str(e)}")

    return Response(
        content=proxy_res.content, 
        status_code=proxy_res.status_code, 
        headers={k: v for k, v in proxy_res.headers.items() if k.lower() not in ["content-encoding", "content-length", "transfer-encoding", "connection"]}
    )