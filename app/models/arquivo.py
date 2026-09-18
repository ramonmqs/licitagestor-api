import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ArquivoProcesso(Base):
    __tablename__ = "arquivos_processo"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    processo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("processos_licitatorios.id", ondelete="CASCADE")
    )
    nome_arquivo: Mapped[str] = mapped_column(String(255))
    chave_armazenamento: Mapped[str] = mapped_column(String(500), unique=True)
    tamanho_bytes: Mapped[int] = mapped_column(BigInteger)
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())