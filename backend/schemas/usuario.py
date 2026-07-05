from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre: str
    password: str


class UsuarioResponse(BaseModel):
    id: int
    email: str
    nombre: str
    activo: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
