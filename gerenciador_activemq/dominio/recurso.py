from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

from gerenciador_activemq.broker.gerenciador_broker import (
    GerenciadorBroker,
    TipoDeOperacao,
)
from gerenciador_activemq.dominio.utilitarios import TipoDeRecurso

NomeDoRecurso = str


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


class OuvinteGerenciadorRecurso(ABC):
    @abstractmethod
    def ao_adicionar_fila(self, nome: NomeDoRecurso):
        raise NotImplementedError

    @abstractmethod
    def ao_adicionar_topico(self, nome: NomeDoRecurso):
        raise NotImplementedError

    @abstractmethod
    def ao_remover_fila(self, nome: NomeDoRecurso):
        raise NotImplementedError

    @abstractmethod
    def ao_remover_topico(self, nome: NomeDoRecurso):
        raise NotImplementedError


class GerenciadorRecurso:
    def __init__(self, gerenciador_broker: GerenciadorBroker):
        self.gerenciador_broker: GerenciadorBroker = gerenciador_broker

        self.informacoes: List[
            InformacaoRecurso
        ] = self._carregar_informacoes_dos_recursos()
        self.mensagens: Dict[NomeDoRecurso, List[Mensagem]] = {}

        self.ouvintes: List[OuvinteGerenciadorRecurso] = []

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
        for ouvinte in self.ouvintes:
            ouvinte.ao_adicionar_fila(nome)

    def adicionar_topico(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.CRIAR_TOPICO, nome_do_recurso=nome
        )
        for ouvinte in self.ouvintes:
            ouvinte.ao_adicionar_topico(nome)

    def remover_fila(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.REMOVER_FILA, nome_do_recurso=nome
        )
        for ouvinte in self.ouvintes:
            ouvinte.ao_remover_fila(nome)

    def remover_topico(self, nome: str):
        self.gerenciador_broker.executar_operacao(
            tipo_de_operacao=TipoDeOperacao.REMOVER_TOPICO, nome_do_recurso=nome
        )
        for ouvinte in self.ouvintes:
            ouvinte.ao_remover_topico(nome)

    def adicionar_ouvinte(self, ouvinte: OuvinteGerenciadorRecurso) -> int:
        self.ouvintes.append(ouvinte)

        return len(self.ouvintes) - 1

    def remover_ouvinte(self, indice: int):
        self.ouvintes.pop(indice)
