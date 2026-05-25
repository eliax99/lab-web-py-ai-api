from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from models.usuario import UsuarioRegistro, UsuarioLogin
from auth.jwt import crear_token

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["bcrypt"])

usuarios = []

@router.post("/registro")
def registro(usuario: UsuarioRegistro):

    for u in usuarios:
        if u["email"] == usuario.email:
            raise HTTPException(status_code=400, detail="Email ya existe")

    password_hash = pwd_context.hash(usuario.password)

    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "password": password_hash
    }

    usuarios.append(nuevo_usuario)

    return {"mensaje": "Usuario registrado"}


@router.post("/login")
def login(datos: UsuarioLogin):

    usuario_encontrado = None

    for u in usuarios:
        if u["email"] == datos.email:
            usuario_encontrado = u

    if not usuario_encontrado:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    password_correcta = pwd_context.verify(
        datos.password,
        usuario_encontrado["password"]
    )

    if not password_correcta:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({
        "user_id": usuario_encontrado["id"],
        "email": usuario_encontrado["email"]
    })

    return {"token": token}