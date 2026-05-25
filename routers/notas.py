from fastapi import APIRouter, HTTPException, Depends
from models.nota import Nota
from auth.jwt import verificar_token

router = APIRouter(prefix="/notas")

notas = []

@router.get("")
def listar_notas(
    buscar: str = "",
    usuario=Depends(verificar_token)
):

    resultado = []

    for nota in notas:

        if nota["user_id"] == usuario["user_id"]:

            if buscar.lower() in nota["contenido"].lower():
                resultado.append(nota)

    return resultado


@router.get("/{id}")
def obtener_nota(
    id: int,
    usuario=Depends(verificar_token)
):

    for nota in notas:

        if nota["id"] == id and nota["user_id"] == usuario["user_id"]:
            return nota

    raise HTTPException(status_code=404, detail="Nota no encontrada")


@router.post("")
def crear_nota(
    nota: Nota,
    usuario=Depends(verificar_token)
):

    nueva_nota = {
        "id": len(notas) + 1,
        "titulo": nota.titulo,
        "contenido": nota.contenido,
        "user_id": usuario["user_id"]
    }

    notas.append(nueva_nota)

    return nueva_nota


@router.put("/{id}")
def editar_nota(
    id: int,
    datos: Nota,
    usuario=Depends(verificar_token)
):

    for nota in notas:

        if nota["id"] == id and nota["user_id"] == usuario["user_id"]:

            nota["titulo"] = datos.titulo
            nota["contenido"] = datos.contenido

            return nota

    raise HTTPException(status_code=404, detail="Nota no encontrada")


@router.delete("/{id}")
def eliminar_nota(
    id: int,
    usuario=Depends(verificar_token)
):

    for nota in notas:

        if nota["id"] == id and nota["user_id"] == usuario["user_id"]:

            notas.remove(nota)

            return {"mensaje": "Nota eliminada"}

    raise HTTPException(status_code=404, detail="Nota no encontrada")