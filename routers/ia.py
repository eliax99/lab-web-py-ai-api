from fastapi import APIRouter, Depends
from auth.jwt import verificar_token
from routers.notas import notas

router = APIRouter(prefix="/api")

chat_historial = {}

@router.get("/search")
def buscar_notas(
    q: str,
    usuario=Depends(verificar_token)
):

    resultados = []

    for nota in notas:

        if (
            nota["user_id"] == usuario["user_id"]
            and q.lower() in nota["contenido"].lower()
        ):
            resultados.append(nota)

    return resultados


@router.post("/chat")
def chat(
    mensaje: dict,
    usuario=Depends(verificar_token)
):

    session_id = mensaje["session_id"]
    texto = mensaje["mensaje"]

    if session_id not in chat_historial:
        chat_historial[session_id] = []

    chat_historial[session_id].append({
        "usuario": texto
    })

    respuesta = f"Has dicho: {texto}"

    chat_historial[session_id].append({
        "ia": respuesta
    })

    return {
        "respuesta": respuesta
    }


@router.get("/chat/history/{session_id}")
def historial(
    session_id: str,
    usuario=Depends(verificar_token)
):

    return chat_historial.get(session_id, [])


@router.get("/context")
def contexto():

    return {
        "nombre_api": "API de notas IA",
        "capacidades": [
            "crear notas",
            "editar notas",
            "buscar notas",
            "chat con historial"
        ]
    }