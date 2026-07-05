from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime


class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo_escala = Column(String, nullable=False)
    puntaje_total = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="evaluaciones")
