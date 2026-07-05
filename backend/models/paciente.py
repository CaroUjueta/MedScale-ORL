from sqlalchemy import Column, Integer, String, Date
from database.db import Base


from sqlalchemy.orm import relationship

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    historial_clinico = Column(String, nullable=True)

    evaluaciones = relationship("Evaluacion", back_populates="paciente")
