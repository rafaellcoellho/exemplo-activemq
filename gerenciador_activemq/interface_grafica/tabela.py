import tkinter
from typing import List

from gerenciador_activemq.dominio.entidades import InformacaoRecurso


class Tabela(tkinter.Frame):
    def __init__(
        self, frame_pai: tkinter.Frame, linhas_iniciais: List[InformacaoRecurso]
    ):
        super().__init__(frame_pai)

        self.cabecalho: List[tkinter.Label] = [
            tkinter.Label(self, text=nome_da_coluna, font=("Arial", 10, "bold"))
            for nome_da_coluna in ["Nome", "Mensagens", "Ações"]
        ]
        self._configurar_cabecalho()

        self.linhas: List[List[tkinter.Widget]] = self._obter_widgets_linhas(
            linhas_iniciais
        )
        self._configurar_linhas()

    def _configurar_cabecalho(self):
        for indice, cabecalho in enumerate(self.cabecalho):
            cabecalho.grid(row=0, column=indice, pady=5, sticky=tkinter.NSEW)

    def _configurar_linhas(self):
        for indice_linha, linha in enumerate(self.linhas):
            for indice_coluna, coluna in enumerate(linha):
                coluna.grid(
                    row=indice_linha + 1,
                    column=indice_coluna,
                    pady=5,
                    sticky=tkinter.NSEW,
                )

    def _obter_widgets_linhas(
        self, linhas_iniciais: List[InformacaoRecurso]
    ) -> List[List[tkinter.Widget]]:
        return [
            [
                tkinter.Label(self, text=linha.nome, font=("Arial", 10), width=20),
                tkinter.Label(
                    self, text=linha.quantidade_de_mensagens, font=("Arial", 10)
                ),
                tkinter.Button(self, text="Remover", font=("Arial", 10), width=20),
            ]
            for linha in linhas_iniciais
        ]
