from fastapi import FastAPI
from routers import pacientes, escalas, auth
from database.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MedScale-ORL API", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(pacientes.router, prefix="/pacientes", tags=["pacientes"])
app.include_router(escalas.router, prefix="/escalas", tags=["escalas"])


@app.get("/")
def root():
    return {"message": "MedScale-ORL API"}
