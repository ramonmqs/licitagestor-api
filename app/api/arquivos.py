import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.storage import excluir_arquivo, gerar_url_download, gerar_url_upload
from app.db.session import get_db
from app.models.arquivo import ArquivoProcesso
from app.models.processo import ProcessoLicitatorio
from app.models.usuario import Usuario
from app.schemas.arquivo import ArquivoConfirmar, ArquivoRead, UploadURLRequest, UploadURLResponse

TAMANHO_MAXIMO_BYTES = 30 * 1024 * 1024

router = APIRouter(prefix="/processos/{processo_id}/arquivos", tags=["arquivos"])


def _buscar_processo(processo_id: uuid.UUID, db: Session) -> ProcessoLicitatorio:
    processo = db.get(ProcessoLicitatorio, processo_id)
    if processo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processo nao encontrado")
    return processo


@router.post("/upload-url", response_model=UploadURLResponse)
def solicitar_url_upload(
    processo_id: uuid.UUID,
    dados: UploadURLRequest,
    usuario: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _buscar_processo(processo_id, db)
    if dados.tamanho_bytes > TAMANHO_MAXIMO_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo excede 30MB")
    chave = f"processos/{processo_id}/{uuid.uuid4()}-{dados.nome_arquivo}"
    return UploadURLResponse(url_upload=gerar_url_upload(chave, dados.content_type), chave_armazenamento=chave)


@router.post("", response_model=ArquivoRead, status_code=status.HTTP_201_CREATED)
def confirmar_upload(
    processo_id: uuid.UUID,
    dados: ArquivoConfirmar,
    usuario: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _buscar_processo(processo_id, db)
    arquivo = ArquivoProcesso(processo_id=processo_id, uploaded_by_id=usuario.id, **dados.model_dump())
    db.add(arquivo)
    db.commit()
    db.refresh(arquivo)
    return arquivo


@router.get("", response_model=list[ArquivoRead])
def listar_arquivos(
    processo_id: uuid.UUID,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _buscar_processo(processo_id, db)
    arquivos = (
        db.query(ArquivoProcesso)
        .filter(ArquivoProcesso.processo_id == processo_id)
        .order_by(ArquivoProcesso.uploaded_at.desc())
        .all()
    )
    resultado = [ArquivoRead.model_validate(a) for a in arquivos]
    for item, arquivo in zip(resultado, arquivos):
        item.url_download = gerar_url_download(arquivo.chave_armazenamento)
    return resultado


@router.delete("/{arquivo_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_arquivo_processo(
    processo_id: uuid.UUID,
    arquivo_id: uuid.UUID,
    usuario: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    arquivo = db.get(ArquivoProcesso, arquivo_id)
    if arquivo is None or arquivo.processo_id != processo_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo nao encontrado")
    excluir_arquivo(arquivo.chave_armazenamento)
    db.delete(arquivo)
    db.commit()