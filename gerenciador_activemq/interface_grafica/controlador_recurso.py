import tkinter
from tkinter import ttk, messagebox
from typing import List

from gerenciador_activemq.dominio.recurso import InformacaoRecurso
from gerenciador_activemq.dominio.utilitarios import TipoDeRecurso
from gerenciador_activemq.interface_grafica.ouvinte import OuvinteControladorRecurso
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
            self.frame_mostrar_recurso,
            linhas_iniciais=recursos_iniciais,
            recurso=recurso,
        )
        self._configurar_interface_mostrar_recurso()

        self.recurso: TipoDeRecurso = recurso
        self.ouvintes: List[OuvinteControladorRecurso] = []

    def _configurar_interface_adicionar_recurso(self):
        self.frame_adicionar_recurso.grid(row=0, column=0)
        self.label_nome_recurso.grid(row=0, column=0)
        self.entrada_nome_recurso.grid(row=0, column=1)
        self.botao_adicionar_recurso.grid(row=0, column=2)

    def _adicionar_recurso(self):
        nome_recurso: str = self.entrada_nome_recurso.get()

        if nome_recurso == "":
            messagebox.showerror("Erro", "Nome não pode ser vazio")
            return
        if self.tabela.linha_ja_existe(nome_recurso):
            messagebox.showerror(
                "Erro",
                f"Já existe {'fila' if self.recurso == TipoDeRecurso.FILA else 'tópico'} com nome {nome_recurso}",
            )
            return

        self.entrada_nome_recurso.delete(0, tkinter.END)
        self.tabela.adicionar_linha(
            linha=InformacaoRecurso(
                nome=nome_recurso,
                quantidade_de_mensagens=0,
                tipo=self.recurso,
            )
        )

        for ouvinte in self.ouvintes:
            ouvinte.ao_adicionar_recurso(nome_recurso, self.recurso)

    def _configurar_interface_mostrar_recurso(self):
        self.separador.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.frame_mostrar_recurso.grid(row=2, column=0, sticky=tkinter.NSEW)
        self.tabela.grid(row=0, column=0, sticky=tkinter.NSEW)

    def adicionar_ouvinte(self, ouvinte: OuvinteControladorRecurso) -> int:
        self.ouvintes.append(ouvinte)
        self.tabela.adicionar_ouvinte(ouvinte)
        return len(self.ouvintes) - 1

    def remover_ouvinte(self, indice: int):
        self.ouvintes.pop(indice)
        self.tabela.remover_ouvinte(indice)

    def adicionar_recurso(self, recurso: InformacaoRecurso):
        self.tabela.adicionar_linha(recurso)
