from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import SECRET_KEY

ALGORITHM = "HS256"

security = HTTPBearer()

def crear_token(data: dict):
    datos = data.copy()

    expiracion = datetime.utcnow() + timedelta(hours=2)

    datos.update({"exp": expiracion})

    token = jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verificar_token(
    credenciales: HTTPAuthorizationCredentials = Depends(security)
):
    token = credenciales.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")