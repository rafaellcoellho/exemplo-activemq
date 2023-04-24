from dataclasses import dataclass

from gerenciador_activemq.dominio.objeto_de_valor import TipoDeRecurso


@dataclass
class InformacaoRecurso:
    nome: str
    quantidade_de_mensagens: int
    tipo: TipoDeRecurso
