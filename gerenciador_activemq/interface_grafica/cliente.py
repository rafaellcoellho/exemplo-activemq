import tkinter
from tkinter import ttk


class InterfaceCliente(tkinter.Frame):
    def __init__(self, frame_pai: tkinter.Toplevel):
        super().__init__(frame_pai)

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
        self.botao_enviar_message: tkinter.Button = tkinter.Button(
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

    def _configurar_interface_de_mensagens(self):
        self.frame_de_mensagens.grid(row=0, column=0, padx=10, pady=10)
        self.visualizador_de_mensagens.grid(row=0, column=0, columnspan=4)
        self.combobox_fila_ou_topico.grid(row=1, column=0, sticky="we")
        self.nome_do_recurso.grid(row=1, column=1, sticky="we")
        self.conteudo_mensagem.grid(row=1, column=2, sticky="we")
        self.botao_enviar_message.grid(row=1, column=3, sticky="we")
        self.label_para_entrada_de_nome_topico_para_assinar.grid(
            row=2, column=0, sticky="we"
        )
        self.entrada_nome_topico_para_assinar.grid(
            row=2, column=1, columnspan=2, sticky="we"
        )
        self.botao_confirmar_assinar_topico.grid(row=2, column=3, sticky="we")

    def _enviar_mensagem(self):
        mensagem: str = self.conteudo_mensagem.get()
        self.conteudo_mensagem.delete(0, tkinter.END)
        print(mensagem)

    def _assinar_topico(self):
        nome_topico: str = self.entrada_nome_topico_para_assinar.get()
        self.entrada_nome_topico_para_assinar.delete(0, tkinter.END)
        print(nome_topico)
