from dataclasses import dataclass
from typing import List, Any, Dict

import requests


@dataclass
class InformacaoRecurso:
    nome: str
    quantidade_de_mensagens: int


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

    def obter_filas(self) -> List[InformacaoRecurso]:
        resposta: GerenciadorBroker.ResultadoAPI = self._ler_objetos(
            "Queue", ["Name", "EnqueueCount"]
        )
        return [
            InformacaoRecurso(
                nome=info_fila["Name"],
                quantidade_de_mensagens=info_fila["EnqueueCount"],
            )
            for info_fila in resposta["value"].values()
        ]

    def obter_topicos(self) -> List[InformacaoRecurso]:
        resposta: GerenciadorBroker.ResultadoAPI = self._ler_objetos(
            "Topic", ["Name", "EnqueueCount"]
        )
        return [
            InformacaoRecurso(
                nome=info_fila["Name"],
                quantidade_de_mensagens=info_fila["EnqueueCount"],
            )
            for info_fila in resposta["value"].values()
        ]
