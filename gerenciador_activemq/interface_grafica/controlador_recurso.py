import tkinter
from tkinter import ttk
from typing import List

from gerenciador_activemq.dominio.entidade import InformacaoRecurso
from gerenciador_activemq.dominio.objeto_de_valor import TipoDeRecurso
from gerenciador_activemq.interface_grafica.tabela import Tabela


class InterfaceControladorRecurso(tkinter.LabelFrame):
    def __init__(
        self,
        frame_pai: tkinter.Frame,
        recurso: TipoDeRecurso,
        recursos_iniciais: List[InformacaoRecurso],
    ):
        super().__init__(
            frame_pai,
            text="gerenciador de filas"
            if recurso == TipoDeRecurso.FILA
            else "gerenciador de tópicos",
        )

        self.frame_adicionar_recurso: tkinter.Frame = tkinter.Frame(self)
        self.label_nome_recurso: tkinter.Label = tkinter.Label(
            self.frame_adicionar_recurso,
            text="Nome da fila:"
            if recurso == TipoDeRecurso.FILA
            else "Nome do tópico:",
            width=15,
        )
        self.entrada_nome_recurso: tkinter.Entry = tkinter.Entry(
            self.frame_adicionar_recurso
        )
        self.botao_adicionar_recurso: tkinter.Button = tkinter.Button(
            self.frame_adicionar_recurso,
            text="Adicionar",
            command=self._adicionar_recurso,
        )
        self._configurar_interface_adicionar_recurso()

        self.separador = ttk.Separator(self, orient=tkinter.HORIZONTAL)
        self.frame_mostrar_recurso: tkinter.Frame = tkinter.Frame(self)
        self.tabela: Tabela = Tabela(
            self.frame_mostrar_recurso, linhas_iniciais=recursos_iniciais
        )
        self._configurar_interface_mostrar_recurso()

    def _configurar_interface_adicionar_recurso(self):
        self.frame_adicionar_recurso.grid(row=0, column=0)
        self.label_nome_recurso.grid(row=0, column=0)
        self.entrada_nome_recurso.grid(row=0, column=1)
        self.botao_adicionar_recurso.grid(row=0, column=2)

    def _adicionar_recurso(self):
        nome_recurso: str = self.entrada_nome_recurso.get()
        self.entrada_nome_recurso.delete(0, tkinter.END)
        print(nome_recurso)

    def _configurar_interface_mostrar_recurso(self):
        self.separador.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.frame_mostrar_recurso.grid(row=2, column=0, sticky=tkinter.NSEW)
        self.tabela.grid(row=0, column=0, sticky=tkinter.NSEW)
