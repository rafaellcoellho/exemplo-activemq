import tkinter
from enum import Enum


class Recurso(Enum):
    FILA = "fila"
    TOPICO = "tópico"


class InterfaceControladorRecurso(tkinter.LabelFrame):
    def __init__(self, frame_pai: tkinter.Frame, recurso: Recurso):
        super().__init__(
            frame_pai,
            text="gerenciador de filas"
            if recurso == Recurso.FILA
            else "gerenciador de tópicos",
        )

        self.frame_adicionar_recurso: tkinter.Frame = tkinter.Frame(self)
        self.label_nome_recurso: tkinter.Label = tkinter.Label(
            self.frame_adicionar_recurso,
            text="Nome da fila:" if recurso == Recurso.FILA else "Nome do tópico:",
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

    def _configurar_interface_adicionar_recurso(self):
        self.frame_adicionar_recurso.grid(row=0, column=0)
        self.label_nome_recurso.grid(row=0, column=0)
        self.entrada_nome_recurso.grid(row=0, column=1)
        self.botao_adicionar_recurso.grid(row=0, column=2)

    def _adicionar_recurso(self):
        nome_recurso: str = self.entrada_nome_recurso.get()
        self.entrada_nome_recurso.delete(0, tkinter.END)
        print(nome_recurso)
