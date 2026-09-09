import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.processo import ProcessoLicitatorio
from app.models.usuario import Usuario
from app.schemas.processo import ProcessoCreate, ProcessoRead

router = APIRouter(prefix="/processos", tags=["processos"])


@router.post("", response_model=ProcessoRead, status_code=status.HTTP_201_CREATED)
def criar_processo(
    dados: ProcessoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    processo = ProcessoLicitatorio(**dados.model_dump(), criado_por_id=usuario.id)
    db.add(processo)
    db.commit()
    db.refresh(processo)
    return processo


@router.get("", response_model=list[ProcessoRead])
def listar_processos(
    usuario: Usuario = Depends(get_current_user), db: Session = Depends(get_db)
):
    return (
        db.query(ProcessoLicitatorio)
        .order_by(ProcessoLicitatorio.created_at.desc())
        .all()
    )


@router.get("/{processo_id}", response_model=ProcessoRead)
def obter_processo(
    processo_id: uuid.UUID,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    processo = db.get(ProcessoLicitatorio, processo_id)
    if processo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Processo nao encontrado"
        )
    return processo