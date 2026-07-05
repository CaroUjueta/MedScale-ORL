from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.paciente import Paciente
from models.escala import Evaluacion
from schemas.escala import EvaluacionCreate, EvaluacionResponse
from utils.dependencies import get_current_user
from models.usuario import Usuario

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/tipos")
def listar_tipos():
    return {
        "escalas": [
            {"id": "vhi", "nombre": "Voice Handicap Index (VHI)", "preguntas": 30},
            {"id": "snot", "nombre": "SNOT-22", "preguntas": 22},
        ]
    }


@router.post("/evaluaciones", response_model=EvaluacionResponse,
             status_code=status.HTTP_201_CREATED)
def crear_evaluacion(data: EvaluacionCreate, db: Session = Depends(get_db),
                     _: Usuario = Depends(get_current_user)):
    paciente = db.query(Paciente).filter(Paciente.id == data.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Paciente no encontrado")
    evaluacion = Evaluacion(
        paciente_id=data.paciente_id,
        tipo_escala=data.tipo_escala,
        puntaje_total=data.puntaje_total,
    )
    db.add(evaluacion)
    db.commit()
    db.refresh(evaluacion)
    return evaluacion


@router.get("/evaluaciones/{paciente_id}", response_model=list[EvaluacionResponse])
def historial_evaluaciones(paciente_id: int, db: Session = Depends(get_db),
                           _: Usuario = Depends(get_current_user)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Paciente no encontrado")
    return db.query(Evaluacion).filter(
        Evaluacion.paciente_id == paciente_id
    ).order_by(Evaluacion.fecha.desc()).all()
