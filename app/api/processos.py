import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.regras_status import transicao_e_valida
from app.db.session import get_db
from app.models.enums import StatusProcesso
from app.models.processo import ProcessoLicitatorio
from app.models.usuario import Usuario
from app.schemas.processo import ProcessoCreate, ProcessoRead, ProcessoStatusUpdate

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


@router.get("/acompanhamento", response_model=list[ProcessoRead])
def listar_acompanhamento(
    usuario: Usuario = Depends(get_current_admin), db: Session = Depends(get_db)
):
    excluidos = {StatusProcesso.AGUARDANDO_DECISAO, StatusProcesso.CANCELADO}
    return (
        db.query(ProcessoLicitatorio)
        .filter(ProcessoLicitatorio.status.not_in(excluidos))
        .order_by(ProcessoLicitatorio.updated_at.desc())
        .all()
    )


@router.post("/{processo_id}/confirmar-participacao", response_model=ProcessoRead)
def confirmar_participacao(
    processo_id: uuid.UUID,
    usuario: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    processo = db.get(ProcessoLicitatorio, processo_id)
    if processo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processo nao encontrado")
    if processo.status != StatusProcesso.AGUARDANDO_DECISAO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="So e possivel confirmar participacao a partir de 'Aguardando decisao'",
        )
    processo.status = StatusProcesso.EM_ANDAMENTO
    db.commit()
    db.refresh(processo)
    return processo


@router.patch("/{processo_id}/status", response_model=ProcessoRead)
def atualizar_status(
    processo_id: uuid.UUID,
    dados: ProcessoStatusUpdate,
    usuario: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    processo = db.get(ProcessoLicitatorio, processo_id)
    if processo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processo nao encontrado")

    if not transicao_e_valida(processo.status, dados.status):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nao e possivel mudar de '{processo.status.value}' para '{dados.status.value}'",
        )

    processo.status = dados.status
    processo.data_hora_retorno = dados.data_hora_retorno
    processo.motivo_diligencia = dados.motivo_diligencia
    db.commit()
    db.refresh(processo)
    return processo


@router.get("/{processo_id}", response_model=ProcessoRead)
def obter_processo(
    processo_id: uuid.UUID,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    processo = db.get(ProcessoLicitatorio, processo_id)
    if processo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processo nao encontrado")
    return processo