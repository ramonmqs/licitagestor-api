from app.models.enums import StatusProcesso

TRANSICOES_PERMITIDAS: dict[StatusProcesso, set[StatusProcesso]] = {
    StatusProcesso.AGUARDANDO_DECISAO: {StatusProcesso.EM_ANDAMENTO, StatusProcesso.CANCELADO},
    StatusProcesso.EM_ANDAMENTO: {
        StatusProcesso.SUSPENSO,
        StatusProcesso.ADIADO,
        StatusProcesso.EM_DILIGENCIA,
        StatusProcesso.CANCELADO,
        StatusProcesso.FINALIZADO,
    },
    StatusProcesso.SUSPENSO: {StatusProcesso.EM_ANDAMENTO, StatusProcesso.CANCELADO},
    StatusProcesso.ADIADO: {StatusProcesso.EM_ANDAMENTO, StatusProcesso.CANCELADO},
    StatusProcesso.EM_DILIGENCIA: {StatusProcesso.EM_ANDAMENTO, StatusProcesso.CANCELADO},
    StatusProcesso.CANCELADO: set(),
    StatusProcesso.FINALIZADO: set(),
}


def transicao_e_valida(status_atual: StatusProcesso, novo_status: StatusProcesso) -> bool:
    return novo_status in TRANSICOES_PERMITIDAS.get(status_atual, set())