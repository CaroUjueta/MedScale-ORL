from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.paciente import Paciente
from schemas.paciente import PacienteCreate, PacienteResponse
from utils.dependencies import get_current_user
from models.usuario import Usuario

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def crear_paciente(data: PacienteCreate, db: Session = Depends(get_db),
                   _: Usuario = Depends(get_current_user)):
    paciente = Paciente(**data.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


@router.get("/", response_model=list[PacienteResponse])
def listar_pacientes(db: Session = Depends(get_db),
                     _: Usuario = Depends(get_current_user)):
    return db.query(Paciente).all()


@router.get("/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db),
                     _: Usuario = Depends(get_current_user)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Paciente no encontrado")
    return paciente


@router.put("/{paciente_id}", response_model=PacienteResponse)
def actualizar_paciente(paciente_id: int, data: PacienteCreate,
                        db: Session = Depends(get_db),
                        _: Usuario = Depends(get_current_user)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Paciente no encontrado")
    for key, value in data.model_dump().items():
        setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db),
                      _: Usuario = Depends(get_current_user)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
