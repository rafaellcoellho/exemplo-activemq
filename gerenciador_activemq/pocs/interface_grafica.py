import tkinter
from dataclasses import dataclass
from typing import Dict, List, NewType, Tuple, Optional, Callable


class NomeDoRecurso(str):
    def __new__(cls, nome: str):
        if len(nome) < 1:
            raise ValueError("Nome da fila não pode ser vazio")
        if len(nome) > 20:
            raise ValueError("Nome da fila não pode ter mais de 20 caracteres")
        return super().__new__(cls, nome)


@dataclass
class Recurso:
    nome: NomeDoRecurso
    quantidade_de_mensagens: int = 0


class GerenciadorDeRecursos:
    def __init__(self):
        self.recursos: Dict[NomeDoRecurso, Recurso] = {}

    def adicionar_recurso(self, recurso: Recurso):
        if recurso.nome in self.recursos:
            raise ValueError("Recurso já existe")
        self.recursos[recurso.nome] = recurso

    def remover_recurso(self, nome_do_recurso: NomeDoRecurso):
        if nome_do_recurso not in self.recursos.keys():
            raise ValueError("Recurso não existe")
        del self.recursos[nome_do_recurso]


class TabelaTkinter(tkinter.Frame):
    Linha = NewType("Linha", List[str])

    def __init__(
        self,
        widget_parent: tkinter.Misc | None,
        cabecalho: Linha,
        callback_ao_remover_recurso: Callable,
    ):
        super().__init__(widget_parent)
        self._cabecalho: TabelaTkinter.Linha = cabecalho
        self._linhas: List[TabelaTkinter.Linha] = []
        self._widgets_das_linhas: List[tkinter.Widget] = []
        self._callback_ao_remover_recurso: Callable = callback_ao_remover_recurso
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
        self._callback_ao_remover_recurso(nome_da_fila=NomeDoRecurso(linha[0]))

    def adiciona_linha(self, linha: Linha):
        self._linhas.append(linha)
        for widget in self._widgets_das_linhas:
            widget.destroy()
        self._configurar_interface()


class InterfaceGerenciamentoDeRecursos:
    def __init__(
        self,
        motor_interface_grafica: tkinter.Tk,
        gerenciador_de_recursos: GerenciadorDeRecursos,
    ):
        self.motor_interface_grafica: tkinter.Tk = motor_interface_grafica
        self.gerenciador_de_recursos: GerenciadorDeRecursos = gerenciador_de_recursos

        self.frame_principal: tkinter.LabelFrame = tkinter.LabelFrame(
            motor_interface_grafica,
            text="gerenciamento de filas",
        )
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10)
        self.tabela_de_recursos: Optional[TabelaTkinter] = None
        self.entrada_para_nome_do_recurso: Optional[tkinter.Entry] = None

        self._configurar_interface_para_adicionar_novo_recurso()
        self._configurar_interface_para_listar_recurso()

    def _configurar_interface_para_adicionar_novo_recurso(self):
        frame_interface_adicionar_recurso: tkinter.Frame = tkinter.Frame(
            self.frame_principal
        )
        frame_interface_adicionar_recurso.grid(row=0, column=0, padx=10, pady=10)

        label_para_nome_do_recurso: tkinter.Label = tkinter.Label(
            frame_interface_adicionar_recurso, text="Nome da fila:"
        )
        label_para_nome_do_recurso.grid(row=0, column=0)

        self.entrada_para_nome_do_recurso = tkinter.Entry(
            frame_interface_adicionar_recurso
        )
        self.entrada_para_nome_do_recurso.grid(row=0, column=1)

        botao_para_adicionar_recurso: tkinter.Button = tkinter.Button(
            frame_interface_adicionar_recurso,
            text="Adicionar",
            command=lambda: self._adicionar_recurso(
                nome_da_fila=self.entrada_para_nome_do_recurso.get()
            ),
        )
        botao_para_adicionar_recurso.grid(row=0, column=2)

    def _configurar_interface_para_listar_recurso(self):
        self.tabela_de_recursos = TabelaTkinter(
            self.frame_principal,
            cabecalho=TabelaTkinter.Linha(["Nome", "Mensagens"]),
            callback_ao_remover_recurso=self._remover_recurso,
        )
        self.tabela_de_recursos.grid(row=1, column=0, padx=10, pady=10)

    def _adicionar_recurso(self, nome_da_fila: str):
        fila: Recurso = Recurso(nome=NomeDoRecurso(nome_da_fila))
        self.gerenciador_de_recursos.adicionar_recurso(recurso=fila)
        if self.tabela_de_recursos is not None:
            self.tabela_de_recursos.adiciona_linha(
                TabelaTkinter.Linha([fila.nome, str(fila.quantidade_de_mensagens)])
            )
        if self.entrada_para_nome_do_recurso is not None:
            self.entrada_para_nome_do_recurso.delete(0, tkinter.END)

    def _remover_recurso(self, nome_da_fila: str):
        self.gerenciador_de_recursos.remover_recurso(
            nome_do_recurso=NomeDoRecurso(nome_da_fila)
        )


def modo_exemplo_interface_grafica():
    gerenciador_de_filas: GerenciadorDeRecursos = GerenciadorDeRecursos()
    gerenciador_de_filas.adicionar_recurso(
        recurso=Recurso(nome=NomeDoRecurso("Fila 1"))
    )

    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("Poc Interface Grafica")

    interface_gerenciamento_de_filas: InterfaceGerenciamentoDeRecursos = (
        InterfaceGerenciamentoDeRecursos(
            motor_interface_grafica=motor_interface_grafica,
            gerenciador_de_recursos=gerenciador_de_filas,
        )
    )

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    modo_exemplo_interface_grafica()
