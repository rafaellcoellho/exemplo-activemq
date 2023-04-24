import tkinter
from tkinter import ttk

import stomp


class OuvinteDeMensagens(stomp.ConnectionListener):
    def __init__(
        self,
        gerenciador_de_cliente: stomp.Connection,
        nome_do_cliente: str,
        interface_cliente,
    ):
        self.nome_do_cliente: str = nome_do_cliente
        self.gerenciador_de_cliente: stomp.Connection = gerenciador_de_cliente
        self.interface_cliente = interface_cliente

    def on_error(self, pacote):
        print("Erro:")
        print(f"\n{pacote}")

    def on_message(self, pacote):
        destino: str = pacote.headers["destination"]
        remetente: str = pacote.headers["sender"]
        mensagem: str = pacote.body

        if destino == f"/queue/{self.nome_do_cliente}":
            self.gerenciador_de_cliente.ack(
                id=pacote.headers["message-id"],
                subscription=pacote.headers["subscription"],
            )

        self.interface_cliente.adicionar_mensagem(f"{remetente}: {mensagem}\n")

    def on_disconnected(self):
        print("Desconectado...")


class InterfaceCliente(tkinter.Frame):
    def __init__(self, frame_pai: tkinter.Toplevel, nome_do_cliente: str):
        super().__init__(frame_pai)

        self.nome_do_cliente: str = nome_do_cliente

        self.frame_de_mensagens: tkinter.LabelFrame = tkinter.LabelFrame(
            self, text="Mensagens"
        )
        self.visualizador_de_mensagens: tkinter.Text = tkinter.Text(
            self.frame_de_mensagens, state=tkinter.DISABLED, width=50, height=20
        )
        self.combobox_fila_ou_topico: ttk.Combobox = ttk.Combobox(
            self.frame_de_mensagens, values=["Fila", "Tópico"], state="readonly"
        )
        self.combobox_fila_ou_topico.current(0)
        self.nome_do_recurso: tkinter.Entry = tkinter.Entry(self.frame_de_mensagens)
        self.conteudo_mensagem: tkinter.Entry = tkinter.Entry(self.frame_de_mensagens)
        self.botao_enviar_mensagem: tkinter.Button = tkinter.Button(
            self.frame_de_mensagens, text="Enviar", command=self._enviar_mensagem
        )
        self.label_para_entrada_de_nome_topico_para_assinar: tkinter.Label = (
            tkinter.Label(self.frame_de_mensagens, text="Nome do tópico para assinar:")
        )
        self.entrada_nome_topico_para_assinar: tkinter.Entry = tkinter.Entry(
            self.frame_de_mensagens,
        )
        self.botao_confirmar_assinar_topico: tkinter.Button = tkinter.Button(
            self.frame_de_mensagens,
            text="Assinar",
            command=self._assinar_topico,
        )
        self._configurar_interface_de_mensagens()

        self.cliente_broker: stomp.Connection = stomp.Connection()
        self.cliente_broker.set_listener(
            name="ouvinte",
            listener=OuvinteDeMensagens(
                gerenciador_de_cliente=self.cliente_broker,
                nome_do_cliente=self.nome_do_cliente,
                interface_cliente=self,
            ),
        )
        self.cliente_broker.connect(username="admin", passcode="admin")
        self.cliente_broker.subscribe(
            destination=f"/queue/{self.nome_do_cliente}",
            id=self.nome_do_cliente,
            ack="client-individual",
        )

    def _configurar_interface_de_mensagens(self):
        self.frame_de_mensagens.grid(row=0, column=0, padx=10, pady=10)
        self.visualizador_de_mensagens.grid(row=0, column=0, columnspan=4)
        self.combobox_fila_ou_topico.grid(row=1, column=0, sticky="we")
        self.nome_do_recurso.grid(row=1, column=1, sticky="we")
        self.conteudo_mensagem.grid(row=1, column=2, sticky="we")
        self.botao_enviar_mensagem.grid(row=1, column=3, sticky="we")
        self.label_para_entrada_de_nome_topico_para_assinar.grid(
            row=2, column=0, sticky="we"
        )
        self.entrada_nome_topico_para_assinar.grid(
            row=2, column=1, columnspan=2, sticky="we"
        )
        self.botao_confirmar_assinar_topico.grid(row=2, column=3, sticky="we")

    def _enviar_mensagem(self):
        fila_para_enviar: str = self.nome_do_recurso.get()
        mensagem: str = self.conteudo_mensagem.get()
        self.conteudo_mensagem.delete(0, tkinter.END)

        recurso = "queue" if self.combobox_fila_ou_topico.get() == "Fila" else "topic"
        self.cliente_broker.send(
            destination=f"/{recurso}/{fila_para_enviar}",
            body=mensagem,
            headers={"sender": self.nome_do_cliente},
        )

    def _assinar_topico(self):
        nome_topico: str = self.entrada_nome_topico_para_assinar.get()
        self.entrada_nome_topico_para_assinar.delete(0, tkinter.END)
        self.cliente_broker.subscribe(
            destination=f"/topic/{nome_topico}",
            id=nome_topico,
        )

    def adicionar_mensagem(self, mensagem: str):
        self.visualizador_de_mensagens.config(state=tkinter.NORMAL)
        self.visualizador_de_mensagens.insert(tkinter.END, mensagem)
        self.visualizador_de_mensagens.config(state=tkinter.DISABLED)
