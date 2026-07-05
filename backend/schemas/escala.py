from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EvaluacionCreate(BaseModel):
    paciente_id: int
    tipo_escala: str
    respuestas: list[int]
    puntaje_total: int


class EvaluacionResponse(BaseModel):
    id: int
    paciente_id: int
    tipo_escala: str
    puntaje_total: int
    fecha: datetime

    model_config = {"from_attributes": True}
