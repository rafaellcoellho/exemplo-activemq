from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any

from gerenciador_activemq.broker.gerenciador_broker import (
    GerenciadorBroker,
    TipoDeOperacao,
)

NomeDoRecurso = str


class TipoDeRecurso(Enum):
    FILA = "fila"
    TOPICO = "tópico"


@dataclass
class Mensagem:
    remetente: str
    conteudo: str
    data: datetime


@dataclass
class InformacaoRecurso:
    nome: str
    quantidade_de_mensagens: int
    tipo: TipoDeRecurso


class GerenciadorRecurso:
    def __init__(self, gerenciador_broker: GerenciadorBroker):
        self.gerenciador_broker: GerenciadorBroker = gerenciador_broker

        self.informacoes: List[
            InformacaoRecurso
        ] = self._carregar_informacoes_dos_recursos()
        self.mensagens: Dict[NomeDoRecurso, List[Mensagem]] = {}

    def _carregar_informacoes_dos_recursos(self) -> List[InformacaoRecurso]:
        filas: List[Dict[str, Any]] = self.gerenciador_broker.obter_recurso(
            tipo=TipoDeRecurso.FILA, atributos=["Name", "EnqueueCount"]
        )
        topicos: List[Dict[str, Any]] = self.gerenciador_broker.obter_recurso(
            tipo=TipoDeRecurso.TOPICO, atributos=["Name", "EnqueueCount"]
        )

        filas_formatadas: List[InformacaoRecurso] = [
            InformacaoRecurso(
                nome=fila["Name"],
                quantidade_de_mensagens=fila["EnqueueCount"],
                tipo=TipoDeRecurso.FILA,
            )
            for fila in filas
        ]
        topicos_formatados: List[InformacaoRecurso] = [
            InformacaoRecurso(
                nome=topico["Name"],
                quantidade_de_mensagens=topico["EnqueueCount"],
                tipo=TipoDeRecurso.TOPICO,
            )
            for topico in topicos
        ]

        return [*filas_formatadas, *topicos_formatados]

    def obter_filas(self) -> List[InformacaoRecurso]:
        return [
            informacao
            for informacao in self.informacoes
            if informacao.tipo == TipoDeRecurso.FILA
        ]

    def obter_topicos(self) -> List[InformacaoRecurso]:
        return [
            informacao
            for informacao in self.informacoes
            if informacao.tipo == TipoDeRecurso.TOPICO
        ]

    def adicionar_fila(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.CRIAR_FILA, nome_do_recurso=nome
        )

    def adicionar_topico(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.CRIAR_TOPICO, nome_do_recurso=nome
        )

    def remover_fila(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.REMOVER_FILA, nome_do_recurso=nome
        )

    def remover_topico(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.REMOVER_TOPICO, nome_do_recurso=nome
        )
