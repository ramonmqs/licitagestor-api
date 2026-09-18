from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.usuario import Usuario
from app.api.processos import router as processos_router
from app.api.arquivos import router as arquivos_router

app = FastAPI(title="LicitaGestor API")
app.include_router(auth_router)
app.include_router(processos_router)
app.include_router(arquivos_router)


@app.get("/")
def read_root():
    return {"projeto": "LicitaGestor", "ambiente": settings.environment}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"banco": "conectado"}


@app.get("/me")
def read_me(usuario: Usuario = Depends(get_current_user)):
    return {"nome": usuario.nome, "email": usuario.email, "perfil": usuario.perfil.value}