import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.models.enums import Modalidade, Portal, StatusProcesso


class ProcessoLicitatorio(Base):
    __tablename__ = "processos_licitatorios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    orgao: Mapped[str] = mapped_column(String(255))
    numero_pregao: Mapped[str] = mapped_column(String(50))
    estado: Mapped[str] = mapped_column(String(2))
    cidade: Mapped[str] = mapped_column(String(120))
    data_certame: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    modalidade: Mapped[Modalidade] = mapped_column(SqlEnum(Modalidade, name="modalidade_pregao"))
    portal: Mapped[Portal] = mapped_column(SqlEnum(Portal, name="portal_pregao"))
    portal_outro: Mapped[str | None] = mapped_column(String(120), nullable=True)
    objeto: Mapped[str] = mapped_column(Text)

    status: Mapped[StatusProcesso] = mapped_column(
        SqlEnum(StatusProcesso, name="status_processo"),
        default=StatusProcesso.AGUARDANDO_DECISAO,
    )
    data_hora_retorno: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    motivo_diligencia: Mapped[str | None] = mapped_column(Text, nullable=True)

    criado_por_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )