import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    LOCAL_FRONTEND_URL: str = "http://localhost:3000"
    
    # URLs de los Microservicios
    LOGIN_SERVICE_URL: str = os.getenv("LOGIN_SERVICE_URL", "")
    CHAT_SERVICE_URL: str = os.getenv("CHAT_SERVICE_URL", "")
    
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_llave_secreta_aqui")
    ALGORITHM: str = "HS256"

settings = Settings()

SERVICES_MAP = {
    "auth": settings.LOGIN_SERVICE_URL,
    "chat": settings.CHAT_SERVICE_URL
}