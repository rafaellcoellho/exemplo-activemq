import argparse
import sys
from typing import Sequence

from gerenciador_activemq import __version__
from gerenciador_activemq.cli.erros import Erro, ModoNaoImplementado
from gerenciador_activemq.pocs.gerenciamento_de_fila import (
    modo_exemplo_gerente_da_fila,
    modo_exemplo_cliente_da_fila,
)


def executa_modo(argumentos: argparse.Namespace):
    if argumentos.modo == "poc_gerenciamento_de_fila":
        if argumentos.papel == "gerente":
            modo_exemplo_gerente_da_fila()
        elif argumentos.papel == "cliente":
            modo_exemplo_cliente_da_fila()
        else:
            raise ModoNaoImplementado
    else:
        raise ModoNaoImplementado


def main(argv: Sequence[str] | None = None):
    argumentos = argv if argv is not None else sys.argv[1:]
    parser_principal = argparse.ArgumentParser(
        prog="gerenciador activemq",
        description="Programa para a disciplina de PPD do curso de eng. da computação no IFCE do semestre 2023.1",
        epilog="Autor: Rafael Coelho (rafaellcoellho@gmail.com)",
        add_help=False,
    )

    versao = f"{__version__}"
    parser_principal.add_argument(
        "-v",
        "--version",
        action="version",
        version=versao,
        help="mostra versão do aplicativo",
    )
    parser_principal.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="mostra ajuda do programa",
    )

    subparsers = parser_principal.add_subparsers(dest="modo")

    # prova de conceito de gerenciamento de filas
    parser_modo_poc_gerenciador_de_fila = subparsers.add_parser(
        "poc_gerenciamento_de_fila", help="poc de gerenciamento de filas do activeMQ"
    )
    subparsers_poc_gerenciador_de_fila = (
        parser_modo_poc_gerenciador_de_fila.add_subparsers(dest="papel")
    )

    subparsers_poc_gerenciador_de_fila.add_parser(
        "gerente", help="iniciar poc com papel de gerenciar o broker"
    )
    subparsers_poc_gerenciador_de_fila.add_parser(
        "cliente", help="iniciar poc com papel de cliente do sistema de filas"
    )

    if len(argumentos) == 0:
        argumentos = ["poc_gerenciamento_de_fila", "gerente"]
    argumentos_formatados = parser_principal.parse_args(argumentos)

    try:
        executa_modo(argumentos=argumentos_formatados)
    except Erro as erro:
        print(erro.mensagem)
        return erro.codigo_de_status
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
