import time
import stomp


def modo_exemplo_ponto_a_ponto_produtor():
    print("executando modo ponto a ponto como produtor")
    gerenciador_de_conexao = stomp.Connection()

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect("admin", "admin", wait=True)
    print("Conectado")

    print("Digite a mensagem para enviar...")
    executando = True
    while executando:
        try:
            mensagem = input("Mensagem: ")
            gerenciador_de_conexao.send(body=mensagem, destination="/queue/teste")
        except KeyboardInterrupt:
            executando = False
    print("Encerrando conexão")

    gerenciador_de_conexao.disconnect()


def modo_exemplo_ponto_a_ponto_consumidor():
    print("executando modo ponto a ponto como consumidor")

    class Consumidor(stomp.ConnectionListener):
        def on_error(self, frame):
            print(f"Mensagem recebido ao dar erro: {frame.body}")

        def on_message(self, frame):
            print(f"Mensagem recebida: {frame.body}")

    gerenciador_de_conexao = stomp.Connection()
    gerenciador_de_conexao.set_listener("", Consumidor())

    print("Iniciando conexão com ActiveMQ")
    gerenciador_de_conexao.connect("admin", "admin", wait=True)
    gerenciador_de_conexao.subscribe(destination="/queue/teste", id="1", ack="auto")
    print("Conectado")

    print("Aguardando mensagens...")
    executando = True
    while executando:
        try:
            time.sleep(2)
            print("Aguardando mensagens...")
        except KeyboardInterrupt:
            executando = False
    print("Encerrando conexão")

    gerenciador_de_conexao.disconnect()
