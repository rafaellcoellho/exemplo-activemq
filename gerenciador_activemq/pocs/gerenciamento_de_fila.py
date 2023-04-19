from typing import Dict, Any, Optional, List

import requests
import stomp
from requests.auth import HTTPBasicAuth


class GerenciadorDoBroker:
    def __init__(self):
        self.url_base: str = "http://127.0.0.1:8161/api/jolokia"
        self.objeto_do_broker: str = (
            "org.apache.activemq:type=Broker,brokerName=localhost"
        )

        self.sessao: requests.Session = requests.Session()
        self.sessao.headers.update({"Origin": "https://127.0.0.1"})
        self.sessao.auth = HTTPBasicAuth(username="admin", password="admin")

    def ler_objetos(self, nome_do_objeto: str, atributos: List[str]) -> Any:
        resultado: requests.Response = self.sessao.post(
            url=self.url_base,
            json={
                "type": "read",
                "mbean": f"{self.objeto_do_broker},destinationType={nome_do_objeto},destinationName=*",
                "attribute": atributos,
            },
        )
        return resultado.json()

    def executar_operacao(self, nome_da_operacao: str, argumentos: List[str]) -> Any:
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


class OuvinteDeMensagens(stomp.ConnectionListener):
    def __init__(self, gerenciador_de_cliente: stomp.Connection, nome_do_cliente: str):
        self.nome_do_cliente: str = nome_do_cliente
        self.gerenciador_de_cliente: stomp.Connection = gerenciador_de_cliente

    def on_error(self, pacote):
        print("Erro:")
        print(f"\n{pacote}")
        print("Escolha uma opção: ", end="")

    def on_message(self, pacote):
        destino: str = pacote.headers["destination"]
        remetente: str = pacote.headers["sender"]
        mensagem: str = pacote.body

        if destino == f"/queue/{self.nome_do_cliente}":
            self.gerenciador_de_cliente.ack(
                id=pacote.headers["message-id"],
                subscription=pacote.headers["subscription"],
            )

        print(f"\n{remetente} disse: {mensagem}", end=" ")
        print("\nEscolha uma opção: ", end="", flush=True)

    def on_disconnected(self):
        print("Desconectado...")


def obter_recurso_do_broker(
    gerenciador_do_broker: GerenciadorDoBroker, recurso: str
) -> Dict[str, Dict[str, str]]:
    resposta: Dict[str, Any] = gerenciador_do_broker.ler_objetos(
        recurso, ["Name", "EnqueueCount"]
    )
    return resposta["value"]


def exibir_recurso(recursos: Dict[str, Dict[str, str]], titulo: str):
    print(f"{titulo:<50} {'Mensagens':<10}")
    for recurso in recursos.values():
        nome: Optional[str] = recurso.get("Name")
        qtd_mensagens: Optional[str] = recurso.get("EnqueueCount")
        print(f"{nome:<50} {qtd_mensagens:<10}")


def executar_operacao_no_broker(
    gerenciador_do_broker: GerenciadorDoBroker,
    operacao: str,
    nome: str,
    msg_sucesso: str,
    msg_erro: str,
):
    resultado: Dict[str, Any] = gerenciador_do_broker.executar_operacao(
        operacao, [nome]
    )
    if resultado.get("status") != 200:
        print(f"{msg_erro}!")
        print(resultado)
    else:
        print(f"{msg_sucesso}!")


def modo_exemplo_gerente_da_fila():
    print("Iniciando gerente...")

    gerenciador_activemq = GerenciadorDoBroker()

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
                    gerenciador_do_broker=gerenciador_activemq,
                    recurso="Queue",
                )
                exibir_recurso(recursos=filas, titulo="Nome da fila")
            elif opcao == "2":
                topicos: Dict[str, Dict[str, str]] = obter_recurso_do_broker(
                    gerenciador_do_broker=gerenciador_activemq,
                    recurso="Topic",
                )
                exibir_recurso(recursos=topicos, titulo="Nome do Tópico")
            elif opcao == "3":
                nome_da_fila: str = input("Nome da fila: ")
                executar_operacao_no_broker(
                    gerenciador_do_broker=gerenciador_activemq,
                    operacao="addQueue",
                    nome=nome_da_fila,
                    msg_sucesso="Fila criada com sucesso!",
                    msg_erro="Erro ao criar fila!",
                )
            elif opcao == "4":
                nome_da_fila: str = input("Nome da fila: ")
                executar_operacao_no_broker(
                    gerenciador_do_broker=gerenciador_activemq,
                    operacao="removeQueue",
                    nome=nome_da_fila,
                    msg_sucesso="Fila removida com sucesso!",
                    msg_erro="Erro ao remover fila!",
                )
            elif opcao == "5":
                nome_do_topico: str = input("Nome do tópico: ")
                executar_operacao_no_broker(
                    gerenciador_do_broker=gerenciador_activemq,
                    operacao="addTopic",
                    nome=nome_do_topico,
                    msg_sucesso="Tópico criado com sucesso!",
                    msg_erro="Erro ao criar tópico!",
                )
            elif opcao == "6":
                nome_do_topico: str = input("Nome do tópico: ")
                executar_operacao_no_broker(
                    gerenciador_do_broker=gerenciador_activemq,
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
    nome_do_cliente: str = input("Nome do cliente: ")

    gerenciador_cliente: stomp.Connection = stomp.Connection()
    gerenciador_cliente.set_listener(
        name="ouvinte",
        listener=OuvinteDeMensagens(
            gerenciador_de_cliente=gerenciador_cliente,
            nome_do_cliente=nome_do_cliente,
        ),
    )
    gerenciador_cliente.connect(username="admin", passcode="admin")
    gerenciador_cliente.subscribe(
        destination=f"/queue/{nome_do_cliente}",
        id=nome_do_cliente,
        ack="client-individual",
    )

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
                topico: str = input("Nome do tópico: ")
                gerenciador_cliente.subscribe(
                    destination=f"/topic/{topico}",
                    id=topico,
                )
            elif opcao == "2":
                fila: str = input("Nome da fila: ")
                mensagem: str = input("Mensagem: ")
                gerenciador_cliente.send(
                    destination=f"/queue/{fila}",
                    body=mensagem,
                    headers={"sender": nome_do_cliente},
                )
            elif opcao == "3":
                topico: str = input("Nome do tópico: ")
                mensagem: str = input("Mensagem: ")
                gerenciador_cliente.send(
                    destination=f"/topic/{topico}",
                    body=mensagem,
                    headers={"sender": nome_do_cliente},
                )
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando cliente...")
    gerenciador_cliente.disconnect()
