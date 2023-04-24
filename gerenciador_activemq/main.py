import tkinter

from gerenciador_activemq.interface_grafica.cliente import InterfaceCliente
from gerenciador_activemq.interface_grafica.controlador_recurso import (
    InterfaceControladorRecurso,
)
from gerenciador_activemq.dominio.recurso import TipoDeRecurso


def main():
    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("gerenciador broker")
    motor_interface_grafica.resizable(False, False)

    frame_gerenciador_broker: tkinter.Frame = tkinter.Frame(motor_interface_grafica)
    interface_controlador_fila: InterfaceControladorRecurso = (
        InterfaceControladorRecurso(
            frame_pai=frame_gerenciador_broker,
            recurso=TipoDeRecurso.FILA,
            recursos_iniciais=[],
        )
    )
    interface_controlador_topico: InterfaceControladorRecurso = (
        InterfaceControladorRecurso(
            frame_pai=frame_gerenciador_broker,
            recurso=TipoDeRecurso.TOPICO,
            recursos_iniciais=[],
        )
    )

    def criar_cliente():
        nome_cliente: str = entrada_nome_cliente.get()
        entrada_nome_cliente.delete(0, tkinter.END)

        # if nome_cliente in [fila.nome for fila in filas]:
        #     messagebox.showerror("Erro", "Já existe um cliente com esse nome")
        #     return

        nova_janela = tkinter.Toplevel(motor_interface_grafica)
        nova_janela.title(f"cliente - {nome_cliente}")
        nova_janela.resizable(False, False)

        interface_cliente: InterfaceCliente = InterfaceCliente(
            frame_pai=nova_janela,
            recursos_disponiveis=[],
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
