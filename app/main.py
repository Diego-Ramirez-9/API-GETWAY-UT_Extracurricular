import uvicorn
import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.routes import router as proxy_router
from app.core.config import settings
from app.core.limiter import limiter

app = FastAPI(title="API Gateway UT Cancún")

# Configuración de Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, settings.LOCAL_FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📝 Logging Middleware Ligero (Sin romper protocolo)
@app.middleware("http")
async def simple_log(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    print(f"LOG: {request.method} {request.url.path} -> {response.status_code} ({duration:.2f}ms)")
    return response

# Ruta de Salud para Railway
@app.get("/ping")
def ping():
    return {"status": "ok", "service": "Gateway"}

app.include_router(proxy_router)

if __name__ == "__main__":
    # IMPORTANTE: host 0.0.0.0 para Railway
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)