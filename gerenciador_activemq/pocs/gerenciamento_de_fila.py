import stomp


def criar_fila(gerenciador_de_conexao: stomp.Connection):
    nome_da_fila: str = input("Digite o nome da fila: ")

    gerenciador_de_conexao.send(
        body="",
        destination=f"/queue/{nome_da_fila}",
        headers={"persistent": "true"},
    )
    print(f"Fila {nome_da_fila} criada com sucesso")


def criar_topico(gerenciador_de_conexao: stomp.Connection):
    nome_do_topico: str = input("Digite o nome do tópico: ")

    gerenciador_de_conexao.send(
        body="",
        destination=f"/topic/{nome_do_topico}",
        headers={"persistent": "true"},
    )
    print(f"Tópico {nome_do_topico} criado com sucesso")


def mostrar_quantidade_de_mensagens(gerenciador_de_conexao: stomp.Connection):
    print("executando mostrar_quantidade_de_mensagens")


def assinar_topico(gerenciador_de_conexao: stomp.Connection):
    print("executando assinar_topico")


def enviar_mensagem_para_cliente(gerenciador_de_conexao: stomp.Connection):
    print("executando enviar_mensagem_para_cliente")


def enviar_mensagem_para_topico(gerenciador_de_conexao: stomp.Connection):
    print("executando enviar_mensagem_para_topico")


def modo_exemplo_gerente_da_fila():
    print("executando gerente da fila")
    gerenciador_de_conexao: stomp.Connection = stomp.Connection()

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect(username="admin", passcode="admin", wait=True)
    print("Conectado")

    executando: bool = True
    while executando:
        try:
            print("=====================================")
            print("1 - Criar fila")
            print("2 - Criar tópico")
            print("3 - Mostrar quantidade de mensagens nas filas/tópicos")
            print("0 - Sair")
            print("=====================================")
            opcao: str = input("Escolha uma opção: ")
            if opcao == "1":
                criar_fila(gerenciador_de_conexao)
            elif opcao == "2":
                criar_topico(gerenciador_de_conexao)
            elif opcao == "3":
                mostrar_quantidade_de_mensagens(gerenciador_de_conexao)
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando conexão")
    gerenciador_de_conexao.disconnect()
    print("Encerrado")


def modo_exemplo_cliente_da_fila():
    print("executando cliente da fila")
    gerenciador_de_conexao: stomp.Connection = stomp.Connection()

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect(username="admin", passcode="admin", wait=True)
    print("Conectado")

    executando: bool = True
    while executando:
        try:
            print("=====================================")
            print("1 - Assinar tópico")
            print("2 - Enviar mensagem para outro cliente")
            print("3 - Enviar mensagem para tópico")
            print("0 - Sair")
            print("=====================================")
            opcao: str = input("Escolha uma opção: ")
            if opcao == "1":
                assinar_topico(gerenciador_de_conexao)
            elif opcao == "2":
                enviar_mensagem_para_cliente(gerenciador_de_conexao)
            elif opcao == "3":
                enviar_mensagem_para_topico(gerenciador_de_conexao)
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando conexão")
    gerenciador_de_conexao.disconnect()
    print("Encerrado")
