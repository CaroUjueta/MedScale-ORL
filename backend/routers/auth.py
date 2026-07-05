from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioResponse, Token, LoginRequest
from utils.security import hash_password, verify_password, create_access_token
from utils.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(data: UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )
    usuario = Usuario(
        email=data.email,
        nombre=data.nombre,
        password_hash=hash_password(data.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )
    token = create_access_token({"sub": str(usuario.id), "email": usuario.email})
    return Token(access_token=token)


@router.get("/me", response_model=UsuarioResponse)
def me(usuario: Usuario = Depends(get_current_user)):
    return usuario
