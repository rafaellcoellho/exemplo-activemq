import tkinter
from dataclasses import dataclass
from datetime import datetime
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
        frame_principal: tkinter.LabelFrame,
        nome_do_recurso: str,
    ):
        self.motor_interface_grafica: tkinter.Tk = motor_interface_grafica
        self.gerenciador_de_recursos: GerenciadorDeRecursos = gerenciador_de_recursos

        self.frame_principal: tkinter.LabelFrame = frame_principal
        self.tabela_de_recursos: Optional[TabelaTkinter] = None
        self.entrada_para_nome_do_recurso: Optional[tkinter.Entry] = None
        self.nome_do_recurso: str = nome_do_recurso

        self._configurar_interface_para_adicionar_novo_recurso()
        self._configurar_interface_para_listar_recurso()

    def _configurar_interface_para_adicionar_novo_recurso(self):
        frame_interface_adicionar_recurso: tkinter.Frame = tkinter.Frame(
            self.frame_principal
        )
        frame_interface_adicionar_recurso.grid(row=0, column=0, padx=10, pady=10)

        label_para_nome_do_recurso: tkinter.Label = tkinter.Label(
            frame_interface_adicionar_recurso, text=f"Nome da {self.nome_do_recurso}:"
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


def obter_mensagens_formatadas_para_mostrar(mensagens: List[dict]) -> str:
    mensagens_formatadas: str = ""
    for mensagem in mensagens:
        horario: datetime = datetime.strptime(mensagem["hora_envio"], "%H:%M:%S")
        mensagens_formatadas += (
            f"{horario} {mensagem['remetente']}: {mensagem['conteudo']}\n"
        )
    return mensagens_formatadas


class InterfaceCliente:
    def __init__(
        self, motor_interface_grafica: tkinter.Tk, frame_principal: tkinter.LabelFrame
    ):
        self.motor_interface_grafica: tkinter.Tk = motor_interface_grafica
        self.frame_principal: tkinter.LabelFrame = frame_principal

        self.frame_dos_seletores: tkinter.Frame = tkinter.Frame(self.frame_principal)
        self.frame_de_mensagens: tkinter.Frame = tkinter.Frame(self.frame_principal)

        self.seletor_de_fila: tkinter.Listbox = tkinter.Listbox(
            self.frame_dos_seletores
        )
        self.seletor_de_topico: tkinter.Listbox = tkinter.Listbox(
            self.frame_dos_seletores
        )
        self.visualizador_de_mensagens: tkinter.Text = tkinter.Text(
            self.frame_de_mensagens, state=tkinter.DISABLED, width=50, height=20
        )
        self.entrada_de_texto_para_mensagem: tkinter.Entry = tkinter.Entry(
            self.frame_de_mensagens
        )
        self.botao_enviar_message: tkinter.Button = tkinter.Button(
            self.frame_de_mensagens, text="Enviar"
        )

        self._configurar_interface_seletor_de_recursos()
        self._configurar_interface_de_mensagens()

    def _configurar_interface_seletor_de_recursos(self):
        self.frame_dos_seletores.grid(row=0, column=0, padx=10, pady=10)
        self.seletor_de_fila.grid(row=0, column=0)
        self.seletor_de_topico.grid(row=1, column=0)

        self.seletor_de_fila.bind("<<ListboxSelect>>", self._mostrar_mensagens)
        self.seletor_de_topico.bind("<<ListboxSelect>>", self._mostrar_mensagens)

    def _configurar_interface_de_mensagens(self):
        self.frame_de_mensagens.grid(row=0, column=1, padx=10, pady=10)
        self.visualizador_de_mensagens.grid(row=0, column=0, columnspan=2)
        self.entrada_de_texto_para_mensagem.grid(row=1, column=0, sticky="we")
        self.botao_enviar_message.grid(row=1, column=1, sticky="we")

    def _mostrar_mensagens(self, evento: tkinter.Event):
        self.visualizador_de_mensagens.delete(1.0, tkinter.END)

        widget_selecionado: tkinter.Listbox = evento.widget
        if len(widget_selecionado.curselection()) == 0:
            return
        indice_selecionado: int = widget_selecionado.curselection()[0]
        nome_do_recurso: str = widget_selecionado.get(indice_selecionado)
        print(f"fila selecionada: {nome_do_recurso}")

        exemplo_de_mensagens = [
            {
                "remetente": "cliente1",
                "conteudo": "mensagem 1",
                "hora_envio": datetime.utcnow(),
            },
            {
                "remetente": "cliente2",
                "conteudo": "mensagem 2",
                "hora_envio": datetime.utcnow(),
            },
        ]

        mensagens_formatadas_para_mostrar: str = (
            obter_mensagens_formatadas_para_mostrar(exemplo_de_mensagens)
        )
        self.visualizador_de_mensagens.insert(
            tkinter.END, mensagens_formatadas_para_mostrar
        )


def instanciar_novo_cliente(motor_interface_grafica: tkinter.Tk, nome_do_cliente: str):
    nova_janela = tkinter.Toplevel(motor_interface_grafica)
    nova_janela.title(f"cliente - {nome_do_cliente}")
    nova_janela.resizable(False, False)

    interface_cliente: InterfaceCliente = InterfaceCliente(
        motor_interface_grafica=motor_interface_grafica,
        frame_principal=tkinter.LabelFrame(nova_janela, text=nome_do_cliente),
    )
    interface_cliente.frame_principal.grid(row=0, column=0, padx=10, pady=10)


def modo_exemplo_interface_grafica():
    gerenciador_de_filas: GerenciadorDeRecursos = GerenciadorDeRecursos()
    gerenciador_de_topicos: GerenciadorDeRecursos = GerenciadorDeRecursos()

    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("poc interface grafica")
    motor_interface_grafica.resizable(False, False)

    frame_principal_filas: tkinter.LabelFrame = tkinter.LabelFrame(
        motor_interface_grafica, text="Gerenciamento de filas"
    )
    frame_principal_filas.grid(row=0, column=0, padx=10, pady=10)
    interface_gerenciamento_de_filas: InterfaceGerenciamentoDeRecursos = (
        InterfaceGerenciamentoDeRecursos(
            motor_interface_grafica=motor_interface_grafica,
            gerenciador_de_recursos=gerenciador_de_filas,
            frame_principal=frame_principal_filas,
            nome_do_recurso="fila",
        )
    )

    frame_principal_topicos: tkinter.LabelFrame = tkinter.LabelFrame(
        motor_interface_grafica, text="Gerenciamento de tópicos"
    )
    frame_principal_topicos.grid(row=0, column=1, padx=10, pady=10)
    interface_gerenciamento_de_topicos: InterfaceGerenciamentoDeRecursos = (
        InterfaceGerenciamentoDeRecursos(
            motor_interface_grafica=motor_interface_grafica,
            gerenciador_de_recursos=gerenciador_de_topicos,
            frame_principal=frame_principal_topicos,
            nome_do_recurso="topico",
        )
    )

    interface_criar_novo_cliente: tkinter.LabelFrame = tkinter.LabelFrame(
        motor_interface_grafica, text="Criar novo cliente"
    )
    interface_criar_novo_cliente.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    entrada_para_nome_do_cliente: tkinter.Entry = tkinter.Entry(
        interface_criar_novo_cliente,
    )
    entrada_para_nome_do_cliente.grid(row=0, column=0, padx=10, pady=10)
    botao_para_criar_novo_cliente: tkinter.Button = tkinter.Button(
        interface_criar_novo_cliente,
        text="criar",
        command=lambda: instanciar_novo_cliente(
            motor_interface_grafica, entrada_para_nome_do_cliente.get()
        ),
    )
    botao_para_criar_novo_cliente.grid(row=0, column=1, padx=10, pady=10)

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    modo_exemplo_interface_grafica()
