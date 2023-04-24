import tkinter
from typing import List

from gerenciador_activemq.dominio.recurso import InformacaoRecurso
from gerenciador_activemq.dominio.utilitarios import TipoDeRecurso
from gerenciador_activemq.interface_grafica.ouvinte import OuvinteControladorRecurso


class Tabela(tkinter.Frame):
    def __init__(
        self,
        frame_pai: tkinter.Frame,
        linhas_iniciais: List[InformacaoRecurso],
        recurso: TipoDeRecurso,
    ):
        super().__init__(frame_pai)

        self.cabecalho: List[tkinter.Label] = [
            tkinter.Label(self, text=nome_da_coluna, font=("Arial", 10, "bold"))
            for nome_da_coluna in ["Nome", "Mensagens", "Ações"]
        ]
        self._configurar_cabecalho()

        self.widgets_das_linhas: List[List[tkinter.Widget]] = []
        self.linhas: List[InformacaoRecurso] = linhas_iniciais
        self._reconstruir_linhas()

        self.recurso: TipoDeRecurso = recurso
        self.ouvintes: List[OuvinteControladorRecurso] = []

    def _configurar_cabecalho(self):
        for indice, cabecalho in enumerate(self.cabecalho):
            cabecalho.grid(row=0, column=indice, pady=5, sticky=tkinter.NSEW)

    def _configurar_linhas(self):
        for indice_linha, linha in enumerate(self.widgets_das_linhas):
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
                tkinter.Button(
                    self,
                    text="Remover",
                    font=("Arial", 10),
                    width=20,
                    command=lambda: self._remover_recurso(linha.nome, indice),
                ),
            ]
            for indice, linha in enumerate(linhas_iniciais)
        ]

    def _remover_recurso(self, nome: str, indice: int):
        self.linhas.pop(indice)
        self._reconstruir_linhas()
        for ouvinte in self.ouvintes:
            ouvinte.ao_remover_recurso(
                nome=nome,
                tipo=self.recurso,
            )

    def _reconstruir_linhas(self):
        if len(self.widgets_das_linhas) > 0:
            for linha in self.widgets_das_linhas:
                for widget in linha:
                    widget.destroy()
        self.widgets_das_linhas = self._obter_widgets_linhas(self.linhas)
        self._configurar_linhas()

    def adicionar_ouvinte(self, ouvinte: OuvinteControladorRecurso) -> int:
        self.ouvintes.append(ouvinte)
        return len(self.ouvintes) - 1

    def remover_ouvinte(self, indice: int):
        self.ouvintes.pop(indice)

    def adicionar_linha(self, linha: InformacaoRecurso):
        self.linhas.append(linha)
        self._reconstruir_linhas()
