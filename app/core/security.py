from jose import jwt, JWTError
from fastapi import HTTPException
from app.core.config import settings

def verify_gateway_token(token: str):
    """Verifica el token en la puerta del Gateway."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401, 
            detail="GATEWAY: Token inválido o expirado."
        )