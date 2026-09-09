import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import Modalidade, Portal, StatusProcesso


class ProcessoCreate(BaseModel):
    orgao: str
    numero_pregao: str
    estado: str
    cidade: str
    data_certame: datetime
    modalidade: Modalidade
    portal: Portal
    portal_outro: str | None = None
    objeto: str

    @model_validator(mode="after")
    def valida_portal_outro(self):
        if self.portal == Portal.OUTROS and not self.portal_outro:
            raise ValueError("Informe o nome do portal quando 'Outros' for selecionado")
        return self


class ProcessoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    orgao: str
    numero_pregao: str
    estado: str
    cidade: str
    data_certame: datetime
    modalidade: Modalidade
    portal: Portal
    portal_outro: str | None
    objeto: str
    status: StatusProcesso
    data_hora_retorno: datetime | None
    motivo_diligencia: str | None
    criado_por_id: uuid.UUID
    created_at: datetime