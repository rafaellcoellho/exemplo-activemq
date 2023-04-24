import tkinter
from tkinter import messagebox

from gerenciador_activemq.broker.gerenciador_broker import GerenciadorBroker
from gerenciador_activemq.dominio.recurso import (
    GerenciadorRecurso,
    NomeDoRecurso,
    OuvinteGerenciadorRecurso,
    InformacaoRecurso,
)
from gerenciador_activemq.dominio.utilitarios import TipoDeRecurso
from gerenciador_activemq.interface_grafica.cliente import InterfaceCliente
from gerenciador_activemq.interface_grafica.controlador_recurso import (
    InterfaceControladorRecurso,
)
from gerenciador_activemq.interface_grafica.ouvinte import OuvinteControladorRecurso


class OuvinteInterfaceControladorRecurso(OuvinteControladorRecurso):
    def __init__(self, gerenciador_recurso: GerenciadorRecurso):
        self.gerenciador_recurso: GerenciadorRecurso = gerenciador_recurso

    def ao_adicionar_recurso(self, nome: NomeDoRecurso, tipo: TipoDeRecurso):
        if tipo == TipoDeRecurso.FILA:
            self.gerenciador_recurso.adicionar_fila(nome)
        elif tipo == TipoDeRecurso.TOPICO:
            self.gerenciador_recurso.adicionar_topico(nome)

    def ao_remover_recurso(self, nome: NomeDoRecurso, tipo: TipoDeRecurso):
        if tipo == TipoDeRecurso.FILA:
            self.gerenciador_recurso.remover_fila(nome)
        elif tipo == TipoDeRecurso.TOPICO:
            self.gerenciador_recurso.remover_topico(nome)


class OuvinteRecurso(OuvinteGerenciadorRecurso):
    def __init__(
        self,
        interface_controlador_filas: InterfaceControladorRecurso,
        interface_controlador_topico: InterfaceControladorRecurso,
    ):
        self.interface_controlador_filas: InterfaceControladorRecurso = (
            interface_controlador_filas
        )
        self.interface_controlador_topico: InterfaceControladorRecurso = (
            interface_controlador_topico
        )

    def ao_adicionar_fila(self, nome: NomeDoRecurso):
        self.interface_controlador_filas.adicionar_recurso(
            recurso=InformacaoRecurso(
                nome=nome, quantidade_de_mensagens=0, tipo=TipoDeRecurso.FILA
            )
        )

    def ao_adicionar_topico(self, nome: NomeDoRecurso):
        self.interface_controlador_topico.adicionar_recurso(
            recurso=InformacaoRecurso(
                nome=nome, quantidade_de_mensagens=0, tipo=TipoDeRecurso.TOPICO
            )
        )

    def ao_remover_fila(self, nome: NomeDoRecurso):
        pass

    def ao_remover_topico(self, nome: NomeDoRecurso):
        pass


def main():
    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("gerenciador broker")
    motor_interface_grafica.resizable(False, False)

    gerenciador_recurso: GerenciadorRecurso = GerenciadorRecurso(
        gerenciador_broker=GerenciadorBroker(
            url_base="http://127.0.0.1:8161/api/jolokia",
            nome_do_broker="localhost",
        ),
    )

    frame_gerenciador_broker: tkinter.Frame = tkinter.Frame(motor_interface_grafica)
    interface_controlador_fila: InterfaceControladorRecurso = (
        InterfaceControladorRecurso(
            frame_pai=frame_gerenciador_broker,
            recurso=TipoDeRecurso.FILA,
            recursos_iniciais=gerenciador_recurso.obter_filas(),
        )
    )
    interface_controlador_fila.adicionar_ouvinte(
        ouvinte=OuvinteInterfaceControladorRecurso(gerenciador_recurso)
    )
    interface_controlador_topico: InterfaceControladorRecurso = (
        InterfaceControladorRecurso(
            frame_pai=frame_gerenciador_broker,
            recurso=TipoDeRecurso.TOPICO,
            recursos_iniciais=gerenciador_recurso.obter_topicos(),
        )
    )
    interface_controlador_topico.adicionar_ouvinte(
        ouvinte=OuvinteInterfaceControladorRecurso(gerenciador_recurso)
    )

    gerenciador_recurso.adicionar_ouvinte(
        ouvinte=OuvinteRecurso(
            interface_controlador_filas=interface_controlador_fila,
            interface_controlador_topico=interface_controlador_topico,
        )
    )

    def criar_cliente():
        nome_cliente: str = entrada_nome_cliente.get()
        entrada_nome_cliente.delete(0, tkinter.END)

        if nome_cliente in [fila.nome for fila in gerenciador_recurso.obter_filas()]:
            messagebox.showerror("Erro", "Já existe um cliente com esse nome")
            return

        nova_janela = tkinter.Toplevel(motor_interface_grafica)
        nova_janela.title(f"cliente - {nome_cliente}")
        nova_janela.resizable(False, False)

        gerenciador_recurso.adicionar_fila(nome_cliente)
        interface_cliente: InterfaceCliente = InterfaceCliente(
            frame_pai=nova_janela,
            nome_do_cliente=nome_cliente,
        )

        interface_cliente.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.NSEW)

    frame_criar_cliente: tkinter.LabelFrame = tkinter.LabelFrame(
        motor_interface_grafica, text="Criar cliente"
    )
    label_nome_cliente: tkinter.Label = tkinter.Label(
        frame_criar_cliente, text="Nome do cliente:", width=20
    )
    entrada_nome_cliente: tkinter.Entry = tkinter.Entry(frame_criar_cliente)
    botao_criar_cliente: tkinter.Button = tkinter.Button(
        frame_criar_cliente, text="Criar", command=criar_cliente
    )

    frame_gerenciador_broker.grid(row=0, column=0, padx=10, pady=10)
    interface_controlador_fila.grid(row=0, column=0, sticky=tkinter.NSEW)
    interface_controlador_topico.grid(row=1, column=0, sticky=tkinter.NSEW)

    frame_criar_cliente.grid(row=1, column=0, padx=10, pady=10)
    label_nome_cliente.grid(row=0, column=0)
    entrada_nome_cliente.grid(row=0, column=1)
    botao_criar_cliente.grid(row=0, column=2)

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    main()
