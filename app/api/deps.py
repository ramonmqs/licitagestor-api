import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decodificar_access_token
from app.db.session import get_db
from app.models.enums import Perfil
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    usuario_id = decodificar_access_token(token)
    if usuario_id is None:
        raise credenciais_invalidas

    usuario = db.get(Usuario, uuid.UUID(usuario_id))
    if usuario is None:
        raise credenciais_invalidas
    return usuario


def get_current_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.perfil != Perfil.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao administrador",
        )
    return usuario