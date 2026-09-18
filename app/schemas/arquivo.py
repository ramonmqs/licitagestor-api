import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UploadURLRequest(BaseModel):
    nome_arquivo: str
    content_type: str
    tamanho_bytes: int


class UploadURLResponse(BaseModel):
    url_upload: str
    chave_armazenamento: str


class ArquivoConfirmar(BaseModel):
    nome_arquivo: str
    chave_armazenamento: str
    tamanho_bytes: int


class ArquivoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome_arquivo: str
    tamanho_bytes: int
    uploaded_by_id: uuid.UUID
    uploaded_at: datetime
    url_download: str | None = None