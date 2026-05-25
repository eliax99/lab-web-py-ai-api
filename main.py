from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.notas import router as notas_router
from routers.ia import router as ia_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(notas_router)
app.include_router(ia_router)


@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}