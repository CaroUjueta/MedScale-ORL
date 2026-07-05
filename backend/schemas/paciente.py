from pydantic import BaseModel
from datetime import date
from typing import Optional


class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    historial_clinico: Optional[str] = None


class PacienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    historial_clinico: Optional[str] = None

    model_config = {"from_attributes": True}
