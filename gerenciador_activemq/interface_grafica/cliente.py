import tkinter
from typing import List

from gerenciador_activemq.dominio.entidades import InformacaoRecurso
from gerenciador_activemq.dominio.objetos_de_valor import TipoDeRecurso


class InterfaceCliente(tkinter.Frame):
    def __init__(
        self, frame_pai: tkinter.Toplevel, recursos_disponiveis: List[InformacaoRecurso]
    ):
        super().__init__(frame_pai)

        self.frame_do_seletor_de_recurso: tkinter.LabelFrame = tkinter.LabelFrame(
            self, text="Recursos"
        )
        self.seletor_de_recurso: tkinter.Listbox = tkinter.Listbox(
            self.frame_do_seletor_de_recurso, width=30, height=21
        )
        self._adicionar_recursos_a_lista(recursos_disponiveis)
        self._configurar_interface_dos_seletores()

        self.frame_de_mensagens: tkinter.LabelFrame = tkinter.LabelFrame(
            self, text="Mensagens"
        )
        self.visualizador_de_mensagens: tkinter.Text = tkinter.Text(
            self.frame_de_mensagens, state=tkinter.DISABLED, width=50, height=20
        )
        self.entrada_de_texto_para_mensagem: tkinter.Entry = tkinter.Entry(
            self.frame_de_mensagens
        )
        self.botao_enviar_message: tkinter.Button = tkinter.Button(
            self.frame_de_mensagens, text="Enviar", command=self._enviar_mensagem
        )
        self._configurar_interface_de_mensagens()

    def _configurar_interface_dos_seletores(self):
        self.frame_do_seletor_de_recurso.grid(row=0, column=0, padx=10, pady=10)
        self.seletor_de_recurso.grid(row=0, column=0)

        self.seletor_de_recurso.bind("<<ListboxSelect>>", self._ao_selecionar_recurso)

    def _configurar_interface_de_mensagens(self):
        self.frame_de_mensagens.grid(row=0, column=1, padx=10, pady=10)
        self.visualizador_de_mensagens.grid(row=0, column=0, columnspan=2)
        self.entrada_de_texto_para_mensagem.grid(row=1, column=0, sticky="we")
        self.botao_enviar_message.grid(row=1, column=1, sticky="we")

    def _enviar_mensagem(self):
        mensagem: str = self.entrada_de_texto_para_mensagem.get()
        self.entrada_de_texto_para_mensagem.delete(0, tkinter.END)
        print(mensagem)

    def _adicionar_recursos_a_lista(
        self, recursos_disponiveis: List[InformacaoRecurso]
    ):
        for recurso in recursos_disponiveis:
            tipo_de_recurso: str = "F" if recurso.tipo == TipoDeRecurso.FILA else "T"
            self.seletor_de_recurso.insert(
                tkinter.END, f"{tipo_de_recurso} | {recurso.nome}"
            )

    def _ao_selecionar_recurso(self, evento: tkinter.Event):
        widget_selecionado: tkinter.Listbox = evento.widget
        if len(widget_selecionado.curselection()) == 0:
            return
        indice_selecionado: int = widget_selecionado.curselection()[0]

        tipo = (
            "fila"
            if widget_selecionado.get(indice_selecionado).split(" | ")[0] == "F"
            else "topico"
        )
        nome_do_recurso: str = widget_selecionado.get(indice_selecionado).split(" | ")[
            1
        ]
        print(f"Selecionado {tipo} {nome_do_recurso}")

        self.visualizador_de_mensagens.delete(1.0, tkinter.END)
