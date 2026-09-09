from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import criar_access_token, verificar_senha
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    usuario = (
        db.query(Usuario)
        .filter(func.lower(Usuario.nome) == form_data.username.strip().lower())
        .first()
    )
    if usuario is None or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome ou senha incorretos",
        )
    return Token(access_token=criar_access_token(str(usuario.id)))