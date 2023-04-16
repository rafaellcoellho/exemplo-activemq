import stomp


def listar_filas_e_qtd_mensagens(gerenciador_de_conexao: stomp.Connection):
    print("executando listar_filas_e_qtd_mensagens")


def listar_topicos_e_qtd_mensagens(gerenciador_de_conexao: stomp.Connection):
    print("executando listar_topicos_e_qtd_mensagens")


def criar_fila(gerenciador_de_conexao: stomp.Connection):
    print("executando criar_fila")


def remover_fila(gerenciador_de_conexao: stomp.Connection):
    print("executando remover_fila")


def criar_topico(gerenciador_de_conexao: stomp.Connection):
    print("executando criar_topico")


def remover_topico(gerenciador_de_conexao: stomp.Connection):
    print("executando remover_topico")


def modo_exemplo_gerente_da_fila():
    gerenciador_de_conexao: stomp.Connection = stomp.Connection()

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect(username="admin", passcode="admin", wait=True)
    print("Conectado")

    executando: bool = True
    while executando:
        try:
            print("=====================================")
            print("1 - Listar filas e quantidades de mensagens")
            print("2 - Listar topicos e quantidades de mensagens")
            print("3 - Criar fila")
            print("4 - Remover fila")
            print("5 - Criar tópico")
            print("6 - Remover tópico")
            print("0 - Sair")
            print("=====================================")

            opcao: str = input("Escolha uma opção: ")

            if opcao == "1":
                listar_filas_e_qtd_mensagens(gerenciador_de_conexao)
            if opcao == "2":
                listar_topicos_e_qtd_mensagens(gerenciador_de_conexao)
            elif opcao == "3":
                criar_fila(gerenciador_de_conexao)
            elif opcao == "4":
                remover_fila(gerenciador_de_conexao)
            elif opcao == "5":
                criar_topico(gerenciador_de_conexao)
            elif opcao == "6":
                remover_topico(gerenciador_de_conexao)
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
