import tkinter
from typing import List, Dict


if __name__ == "__main__":
    print("Poc interface grafica...")

    filas: List[Dict[str, str]] = [
        {
            "name": "fila",
            "quantidade_de_mensagens": "10",
        }
    ]

    def adicionar_fila():
        nome_da_fila: str = entrada_para_nome_da_fila.get()
        filas.append(
            {
                "name": nome_da_fila,
                "quantidade_de_mensagens": "0",
            }
        )

    gerenciador_de_interface_grafica: tkinter.Tk = tkinter.Tk()
    gerenciador_de_interface_grafica.title("Poc Interface Grafica")

    # Interface de gerenciamento de fila
    interface_de_gerenciamento_de_fila: tkinter.Frame = tkinter.Frame(
        gerenciador_de_interface_grafica
    )
    interface_de_gerenciamento_de_fila.grid(row=0, column=0)

    # Interface para adicionar nova fila
    interface_para_adicionar_nova_fila: tkinter.Frame = tkinter.Frame(
        interface_de_gerenciamento_de_fila
    )
    interface_para_adicionar_nova_fila.grid(row=0, column=0)

    label_para_nome_da_fila: tkinter.Label = tkinter.Label(
        interface_para_adicionar_nova_fila, text="Nome da fila:"
    )
    label_para_nome_da_fila.grid(row=0, column=0)
    entrada_para_nome_da_fila: tkinter.Entry = tkinter.Entry(
        interface_para_adicionar_nova_fila
    )
    entrada_para_nome_da_fila.grid(row=0, column=1)
    botao_para_adicionar_fila: tkinter.Button = tkinter.Button(
        interface_para_adicionar_nova_fila,
        text="Adicionar",
        command=adicionar_fila,
    )
    botao_para_adicionar_fila.grid(row=0, column=2)

    gerenciador_de_interface_grafica.mainloop()
