import tkinter
from typing import List

from gerenciador_activemq.broker.gerenciador_broker import (
    GerenciadorBroker,
    InformacaoRecurso,
)
from gerenciador_activemq.interface_grafica.controlador_recurso import (
    Recurso,
    InterfaceControladorRecurso,
)


def main():
    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("gerenciador broker")
    motor_interface_grafica.resizable(False, False)

    gerenciador_broker = GerenciadorBroker(
        url_base="http://127.0.0.1:8161/api/jolokia",
        nome_do_broker="localhost",
    )
    filas: List[InformacaoRecurso] = gerenciador_broker.obter_filas()
    topico: List[InformacaoRecurso] = gerenciador_broker.obter_topicos()

    frame_gerenciador_broker: tkinter.Frame = tkinter.Frame(motor_interface_grafica)
    interface_controlador_fila: InterfaceControladorRecurso = (
        InterfaceControladorRecurso(
            frame_pai=frame_gerenciador_broker,
            recurso=Recurso.FILA,
            recursos_iniciais=filas,
        )
    )
    interface_controlador_topico: InterfaceControladorRecurso = (
        InterfaceControladorRecurso(
            frame_pai=frame_gerenciador_broker,
            recurso=Recurso.TOPICO,
            recursos_iniciais=topico,
        )
    )

    frame_gerenciador_broker.grid(row=0, column=0, padx=10, pady=10)
    interface_controlador_fila.grid(row=0, column=0, sticky=tkinter.NSEW)
    interface_controlador_topico.grid(row=1, column=0, sticky=tkinter.NSEW)

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    main()
