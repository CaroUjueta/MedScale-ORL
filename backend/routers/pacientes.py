from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def listar_pacientes():
    return {"pacientes": []}


@router.get("/{paciente_id}")
def obtener_paciente(paciente_id: int):
    return {"paciente_id": paciente_id}
