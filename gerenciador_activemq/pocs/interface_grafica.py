import tkinter
from dataclasses import dataclass
from typing import Dict


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


class InterfaceGerenciamentoDeFilas:
    def __init__(
        self,
        motor_interface_grafica: tkinter.Tk,
        gerenciador_de_filas: GerenciadorDeFilas,
    ):
        self.motor_interface_grafica: tkinter.Tk = motor_interface_grafica
        self.gerenciador_de_filas: GerenciadorDeFilas = gerenciador_de_filas

        self.frame_principal: tkinter.Frame = tkinter.Frame(motor_interface_grafica)
        self.frame_principal.grid(row=0, column=0)

        self.configurar_interface_para_adicionar_nova_fila()
        self.configurar_interface_para_listar_filas()
        self.configurar_interface_para_remover_fila()

    def configurar_interface_para_adicionar_nova_fila(self):
        frame_interface_adicionar_fila: tkinter.Frame = tkinter.Frame(
            self.frame_principal
        )
        frame_interface_adicionar_fila.grid(row=0, column=0)

        label_para_nome_da_fila: tkinter.Label = tkinter.Label(
            frame_interface_adicionar_fila, text="Nome da fila:"
        )
        label_para_nome_da_fila.grid(row=0, column=0)

        entrada_para_nome_da_fila: tkinter.Entry = tkinter.Entry(
            frame_interface_adicionar_fila
        )
        entrada_para_nome_da_fila.grid(row=0, column=1)

        botao_para_adicionar_fila: tkinter.Button = tkinter.Button(
            frame_interface_adicionar_fila,
            text="Adicionar",
            command=lambda: self.gerenciador_de_filas.adicionar_fila(
                fila=Fila(nome=NomeDaFila(entrada_para_nome_da_fila.get()))
            ),
        )
        botao_para_adicionar_fila.grid(row=0, column=2)

    def configurar_interface_para_listar_filas(self):
        ...

    def configurar_interface_para_remover_fila(self):
        ...


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
