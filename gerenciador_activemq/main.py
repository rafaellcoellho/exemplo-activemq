import tkinter
from typing import List

from gerenciador_activemq.broker.gerenciador_broker import (
    GerenciadorBroker,
    InformacaoRecurso,
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
    print(filas)
    print(topico)

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    main()
