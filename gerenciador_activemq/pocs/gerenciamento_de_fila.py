import json
import re
from typing import Dict, Tuple, Any, List

import requests
from requests.auth import HTTPBasicAuth


def modo_exemplo_gerente_da_fila():
    print("Iniciando gerente...")

    url_base: str = "http://127.0.0.1:8161/api/jolokia"
    objeto_do_broker: str = "org.apache.activemq:type=Broker,brokerName=localhost"

    sessao: requests.Session = requests.Session()
    sessao.headers.update({"Origin": "https://127.0.0.1"})
    sessao.auth = HTTPBasicAuth(username="admin", password="admin")

    executando: bool = True
    while executando:
        try:
            print("==================================================")
            print("1 - Listar filas e quantidades de mensagens")
            print("2 - Listar topicos e quantidades de mensagens")
            print("3 - Criar fila")
            print("4 - Remover fila")
            print("5 - Criar tópico")
            print("6 - Remover tópico")
            print("0 - Sair")
            print("==================================================")

            opcao: str = input("Escolha uma opção: ")

            if opcao == "1":
                resultado: requests.Response = sessao.post(
                    url=url_base,
                    json={
                        "type": "read",
                        "mbean": f"{objeto_do_broker},destinationType=Queue,destinationName=*",
                        "attribute": ["Name", "QueueSize"],
                    },
                )
                resposta: Dict[str, Any] = resultado.json()
                filas: Dict[str, Dict[str, str]] = resposta["value"]
                print(f"{'Nome da fila':<20} {'Mensagens':<10}")
                for fila in filas.values():
                    nome_da_fila: str = fila.get("Name")
                    qtd_mensagens: str = fila.get("QueueSize")
                    print(f"{nome_da_fila:<20} {qtd_mensagens:<10}")
            elif opcao == "2":
                ...
            elif opcao == "3":
                nome_da_fila: str = input("Nome da fila: ")
                resultado: requests.Response = sessao.post(
                    url=url_base,
                    json={
                        "type": "exec",
                        "mbean": objeto_do_broker,
                        "operation": "addQueue",
                        "arguments": [nome_da_fila],
                    },
                )
                if resultado.status_code != 200:
                    print("Erro ao criar fila!")
                    print(resultado.json())
                print("Fila criada com sucesso!")
            elif opcao == "4":
                nome_da_fila: str = input("Nome da fila: ")
                resultado: requests.Response = sessao.post(
                    url=url_base,
                    json={
                        "type": "exec",
                        "mbean": objeto_do_broker,
                        "operation": "removeQueue",
                        "arguments": [nome_da_fila],
                    },
                )
                if resultado.status_code != 200:
                    print("Erro ao remover fila!")
                    print(resultado.json())
                print("Fila removida com sucesso!")
            elif opcao == "5":
                ...
            elif opcao == "6":
                ...
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando gerente...")


def modo_exemplo_cliente_da_fila():
    print(f"cliente")
