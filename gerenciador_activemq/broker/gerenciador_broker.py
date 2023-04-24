from enum import Enum
from typing import List, Any, Dict

import requests

from gerenciador_activemq.dominio.utilitarios import TipoDeRecurso


class TipoDeOperacao(Enum):
    CRIAR_FILA = "addQueue"
    CRIAR_TOPICO = "addTopic"
    REMOVER_FILA = "removeQueue"
    REMOVER_TOPICO = "removeTopic"


class NaoFoiPossivelRealizarOperacao(Exception):
    pass


class GerenciadorBroker:
    ResultadoAPI = Dict[str, Any]

    def __init__(self, url_base: str, nome_do_broker: str):
        self.url_base: str = url_base
        self.objeto_do_broker: str = (
            f"org.apache.activemq:type=Broker,brokerName={nome_do_broker}"
        )

        self.sessao: requests.Session = requests.Session()
        self.sessao.headers.update({"Origin": "https://127.0.0.1"})
        self.sessao.auth = ("admin", "admin")

    def _ler_objetos(self, nome_do_objeto: str, atributos: List[str]) -> ResultadoAPI:
        resultado: requests.Response = self.sessao.post(
            url=self.url_base,
            json={
                "type": "read",
                "mbean": f"{self.objeto_do_broker},destinationType={nome_do_objeto},destinationName=*",
                "attribute": atributos,
            },
        )
        return resultado.json()

    def _executar_operacao(
        self, nome_da_operacao: str, argumentos: List[str]
    ) -> ResultadoAPI:
        resultado: requests.Response = self.sessao.post(
            url=self.url_base,
            json={
                "type": "exec",
                "mbean": self.objeto_do_broker,
                "operation": nome_da_operacao,
                "arguments": argumentos,
            },
        )
        return resultado.json()

    def obter_recurso(
        self, tipo: TipoDeRecurso, atributos: List[str]
    ) -> List[Dict[str, Any]]:
        nome_do_objeto: str = "Queue" if tipo == TipoDeRecurso.FILA else "Topic"
        resposta: GerenciadorBroker.ResultadoAPI = self._ler_objetos(
            nome_do_objeto=nome_do_objeto,
            atributos=atributos,
        )
        return resposta["value"].values()

    def executar_operacao(self, tipo_de_operacao: TipoDeOperacao, nome_do_recurso: str):
        nome_da_operacao: str = tipo_de_operacao.value

        resultado: GerenciadorBroker.ResultadoAPI = self._executar_operacao(
            nome_da_operacao=nome_da_operacao,
            argumentos=[nome_do_recurso],
        )
        if resultado["status"] != 200:
            raise NaoFoiPossivelRealizarOperacao(resultado)
