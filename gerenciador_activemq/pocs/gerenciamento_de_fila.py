from typing import Dict, Any, Optional

import requests
from requests.auth import HTTPBasicAuth


def obter_recurso_do_broker(
    sessao: requests.Session, url_base: str, objeto_do_broker: str, recurso: str
) -> Dict[str, Dict[str, str]]:
    resultado: requests.Response = sessao.post(
        url=url_base,
        json={
            "type": "read",
            "mbean": f"{objeto_do_broker},destinationType={recurso},destinationName=*",
            "attribute": ["Name", "QueueSize"],
        },
    )
    resposta: Dict[str, Any] = resultado.json()
    return resposta["value"]


def exibir_recurso(recursos: Dict[str, Dict[str, str]], titulo: str):
    print(f"{titulo:<50} {'Mensagens':<10}")
    for recurso in recursos.values():
        nome: Optional[str] = recurso.get("Name")
        qtd_mensagens: Optional[str] = recurso.get("QueueSize")
        print(f"{nome:<50} {qtd_mensagens:<10}")


def executar_operacao_no_broker(
    sessao: requests.Session,
    url_base: str,
    objeto_do_broker: str,
    operacao: str,
    nome: str,
    msg_sucesso: str,
    msg_erro: str,
):
    resultado: requests.Response = sessao.post(
        url=url_base,
        json={
            "type": "exec",
            "mbean": objeto_do_broker,
            "operation": operacao,
            "arguments": [nome],
        },
    )
    if resultado.status_code != 200:
        print(f"{msg_erro}!")
        print(resultado.json())
    else:
        print(f"{msg_sucesso}!")


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
                filas: Dict[str, Dict[str, str]] = obter_recurso_do_broker(
                    sessao=sessao,
                    url_base=url_base,
                    objeto_do_broker=objeto_do_broker,
                    recurso="Queue",
                )
                exibir_recurso(recursos=filas, titulo="Nome da fila")
            elif opcao == "2":
                topicos: Dict[str, Dict[str, str]] = obter_recurso_do_broker(
                    sessao=sessao,
                    url_base=url_base,
                    objeto_do_broker=objeto_do_broker,
                    recurso="Topic",
                )
                exibir_recurso(recursos=topicos, titulo="Nome do Tópico")
            elif opcao == "3":
                nome_da_fila: str = input("Nome da fila: ")
                executar_operacao_no_broker(
                    sessao=sessao,
                    url_base=url_base,
                    objeto_do_broker=objeto_do_broker,
                    operacao="addQueue",
                    nome=nome_da_fila,
                    msg_sucesso="Fila criada com sucesso!",
                    msg_erro="Erro ao criar fila!",
                )
            elif opcao == "4":
                nome_da_fila: str = input("Nome da fila: ")
                executar_operacao_no_broker(
                    sessao=sessao,
                    url_base=url_base,
                    objeto_do_broker=objeto_do_broker,
                    operacao="removeQueue",
                    nome=nome_da_fila,
                    msg_sucesso="Fila removida com sucesso!",
                    msg_erro="Erro ao remover fila!",
                )
            elif opcao == "5":
                nome_do_topico: str = input("Nome do tópico: ")
                executar_operacao_no_broker(
                    sessao=sessao,
                    url_base=url_base,
                    objeto_do_broker=objeto_do_broker,
                    operacao="addTopic",
                    nome=nome_do_topico,
                    msg_sucesso="Tópico criado com sucesso!",
                    msg_erro="Erro ao criar tópico!",
                )
            elif opcao == "6":
                nome_do_topico: str = input("Nome do tópico: ")
                executar_operacao_no_broker(
                    sessao=sessao,
                    url_base=url_base,
                    objeto_do_broker=objeto_do_broker,
                    operacao="removeTopic",
                    nome=nome_do_topico,
                    msg_sucesso="Tópico removido com sucesso!",
                    msg_erro="Erro ao remover tópico!",
                )
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando gerente...")


def modo_exemplo_cliente_da_fila():
    print(f"Iniciando cliente...")

    executando: bool = True
    while executando:
        try:
            print("==================================================")
            print("1 - Assinar tópico")
            print("2 - Enviar mensagem para fila")
            print("3 - Enviar mensagem para topico")
            print("0 - Sair")
            print("==================================================")

            opcao: str = input("Escolha uma opção: ")

            if opcao == "1":
                ...
            elif opcao == "2":
                ...
            elif opcao == "3":
                ...
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando cliente...")
