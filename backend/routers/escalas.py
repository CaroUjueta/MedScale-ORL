from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def listar_escalas():
    return {"escalas": ["VHI", "SNOT-22"]}


@router.get("/{escala_id}")
def obtener_escala(escala_id: int):
    return {"escala_id": escala_id}
