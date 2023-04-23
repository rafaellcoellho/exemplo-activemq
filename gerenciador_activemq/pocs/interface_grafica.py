import tkinter
from dataclasses import dataclass
from typing import Dict, List, NewType, Tuple, Optional, Callable


class NomeDaFila(str):
    def __new__(cls, nome: str):
        if len(nome) < 1:
            raise ValueError("Nome da fila não pode ser vazio")
        if len(nome) > 20:
            raise ValueError("Nome da fila não pode ter mais de 20 caracteres")
        return super().__new__(cls, nome)


@dataclass
class Fila:
    nome: NomeDaFila
    quantidade_de_mensagens: int = 0


class GerenciadorDeFilas:
    def __init__(self):
        self.filas: Dict[NomeDaFila, Fila] = {}

    def adicionar_fila(self, fila: Fila):
        if fila.nome in self.filas:
            raise ValueError("Fila já existe")
        self.filas[fila.nome] = fila

    def remover_fila(self, nome_da_fila: NomeDaFila):
        if nome_da_fila not in self.filas.keys():
            raise ValueError("Fila não existe")
        del self.filas[nome_da_fila]


class TabelaTkinter(tkinter.Frame):
    Linha = NewType("Linha", List[str])

    def __init__(
        self,
        widget_parent: tkinter.Misc | None,
        cabecalho: Linha,
        callback_ao_remover_fila: Callable,
    ):
        super().__init__(widget_parent)
        self._cabecalho: TabelaTkinter.Linha = cabecalho
        self._linhas: List[TabelaTkinter.Linha] = []
        self._widgets_das_linhas: List[tkinter.Widget] = []
        self._callback_ao_remover_fila: Callable = callback_ao_remover_fila
        self._configurar_interface()

    def _configurar_interface(self):
        self._configurar_cabecalho()
        self._configurar_linhas()

    def _configurar_cabecalho(self):
        fonte_cabecalho: Tuple[str, int, str] = ("Arial", 10, "bold")
        for indice, titulo in enumerate(self._cabecalho):
            tkinter.Label(self, text=titulo, font=("Arial", 10, "bold")).grid(
                row=0, column=indice
            )

        tkinter.Label(self, text="Ações", font=fonte_cabecalho).grid(
            row=0, column=len(self._cabecalho)
        )

    def _configurar_linhas(self):
        for indice_linha, linha in enumerate(self._linhas):
            for indice_coluna, valor in enumerate(linha):
                label_da_coluna: tkinter.Label = tkinter.Label(self, text=valor)
                label_da_coluna.grid(row=indice_linha + 1, column=indice_coluna)
                self._widgets_das_linhas.append(label_da_coluna)

            botao_para_remover_linha: tkinter.Button = tkinter.Button(
                self,
                text="Remover",
                command=lambda indice=indice_linha: self._remover_linha(indice_linha),
            )
            botao_para_remover_linha.grid(
                row=indice_linha + 1,
                column=len(self._cabecalho),
            )
            self._widgets_das_linhas.append(botao_para_remover_linha)

    def _remover_linha(self, indice: int):
        linha: TabelaTkinter.Linha = self._linhas.pop(indice)
        for widget in self._widgets_das_linhas:
            widget.destroy()
        self._configurar_interface()
        self._callback_ao_remover_fila(nome_da_fila=NomeDaFila(linha[0]))

    def adiciona_linha(self, linha: Linha):
        self._linhas.append(linha)
        for widget in self._widgets_das_linhas:
            widget.destroy()
        self._configurar_interface()


class InterfaceGerenciamentoDeFilas:
    def __init__(
        self,
        motor_interface_grafica: tkinter.Tk,
        gerenciador_de_filas: GerenciadorDeFilas,
    ):
        self.motor_interface_grafica: tkinter.Tk = motor_interface_grafica
        self.gerenciador_de_filas: GerenciadorDeFilas = gerenciador_de_filas

        self.frame_principal: tkinter.LabelFrame = tkinter.LabelFrame(
            motor_interface_grafica,
            text="gerenciamento de filas",
        )
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10)
        self.tabela_de_filas: Optional[TabelaTkinter] = None
        self.entrada_para_nome_da_fila: Optional[tkinter.Entry] = None

        self._configurar_interface_para_adicionar_nova_fila()
        self._configurar_interface_para_listar_filas()

    def _configurar_interface_para_adicionar_nova_fila(self):
        frame_interface_adicionar_fila: tkinter.Frame = tkinter.Frame(
            self.frame_principal
        )
        frame_interface_adicionar_fila.grid(row=0, column=0, padx=10, pady=10)

        label_para_nome_da_fila: tkinter.Label = tkinter.Label(
            frame_interface_adicionar_fila, text="Nome da fila:"
        )
        label_para_nome_da_fila.grid(row=0, column=0)

        self.entrada_para_nome_da_fila = tkinter.Entry(frame_interface_adicionar_fila)
        self.entrada_para_nome_da_fila.grid(row=0, column=1)

        botao_para_adicionar_fila: tkinter.Button = tkinter.Button(
            frame_interface_adicionar_fila,
            text="Adicionar",
            command=lambda: self._adicionar_fila(
                nome_da_fila=self.entrada_para_nome_da_fila.get()
            ),
        )
        botao_para_adicionar_fila.grid(row=0, column=2)

    def _configurar_interface_para_listar_filas(self):
        self.tabela_de_filas = TabelaTkinter(
            self.frame_principal,
            cabecalho=TabelaTkinter.Linha(["Nome", "Mensagens"]),
            callback_ao_remover_fila=self._remover_fila,
        )
        self.tabela_de_filas.grid(row=1, column=0, padx=10, pady=10)

    def _adicionar_fila(self, nome_da_fila: str):
        fila: Fila = Fila(nome=NomeDaFila(nome_da_fila))
        self.gerenciador_de_filas.adicionar_fila(fila=fila)
        if self.tabela_de_filas is not None:
            self.tabela_de_filas.adiciona_linha(
                TabelaTkinter.Linha([fila.nome, str(fila.quantidade_de_mensagens)])
            )
        if self.entrada_para_nome_da_fila is not None:
            self.entrada_para_nome_da_fila.delete(0, tkinter.END)

    def _remover_fila(self, nome_da_fila: str):
        self.gerenciador_de_filas.remover_fila(nome_da_fila=NomeDaFila(nome_da_fila))


def modo_exemplo_interface_grafica():
    gerenciador_de_filas: GerenciadorDeFilas = GerenciadorDeFilas()
    gerenciador_de_filas.adicionar_fila(fila=Fila(nome=NomeDaFila("Fila 1")))

    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("Poc Interface Grafica")

    interface_gerenciamento_de_filas: InterfaceGerenciamentoDeFilas = (
        InterfaceGerenciamentoDeFilas(
            motor_interface_grafica=motor_interface_grafica,
            gerenciador_de_filas=gerenciador_de_filas,
        )
    )

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    modo_exemplo_interface_grafica()
