from pydantic import BaseModel

class Nota(BaseModel):
    titulo: str
    contenido: str