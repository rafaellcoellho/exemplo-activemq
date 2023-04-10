import time
import stomp


def criar_fila(gerenciador_de_conexao):
    print("executando criar_fila")


def criar_topico(gerenciador_de_conexao):
    print("executando criar_topico")


def mostrar_quantidade_de_mensagens(gerenciador_de_conexao):
    print("executando mostrar_quantidade_de_mensagens")


def assinar_topico(gerenciador_de_conexao):
    print("executando assinar_topico")


def enviar_mensagem_para_cliente(gerenciador_de_conexao):
    print("executando enviar_mensagem_para_cliente")


def enviar_mensagem_para_topico(gerenciador_de_conexao):
    print("executando enviar_mensagem_para_topico")


def modo_exemplo_gerente_da_fila():
    print("executando gerente da fila")
    gerenciador_de_conexao = stomp.Connection()

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect("admin", "admin", wait=True)
    print("Conectado")

    executando = True
    while executando:
        try:
            print("=====================================")
            print("1 - Criar fila")
            print("2 - Criar tópico")
            print("3 - Mostrar quantidade de mensagens nas filas/tópicos")
            print("0 - Sair")
            print("=====================================")
            opcao = input("Escolha uma opção: ")
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
    gerenciador_de_conexao = stomp.Connection()

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect("admin", "admin", wait=True)
    print("Conectado")

    executando = True
    while executando:
        try:
            print("=====================================")
            print("1 - Assinar tópico")
            print("2 - Enviar mensagem para outro cliente")
            print("3 - Enviar mensagem para tópico")
            print("0 - Sair")
            print("=====================================")
            opcao = input("Escolha uma opção: ")
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
