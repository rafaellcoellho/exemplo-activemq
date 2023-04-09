import argparse
import sys
from typing import Sequence

from gerenciador_activemq import __version__
from gerenciador_activemq.cli.erros import Erro, ModoNaoImplementado
from gerenciador_activemq.pocs.ponto_a_ponto import (
    modo_exemplo_ponto_a_ponto_produtor,
    modo_exemplo_ponto_a_ponto_consumidor,
)


def executa_modo(argumentos: argparse.Namespace):
    if argumentos.modo == "poc_ponto_a_ponto":
        if argumentos.papel == "produtor":
            modo_exemplo_ponto_a_ponto_produtor()
        elif argumentos.papel == "consumidor":
            modo_exemplo_ponto_a_ponto_consumidor()
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

    # prova de conceito domínio ponto a ponto
    parser_modo_poc_ponto_a_ponto = subparsers.add_parser(
        "poc_ponto_a_ponto", help="poc de domínio ponto a ponto do activeMQ"
    )
    subparsers_poc_ponto_a_ponto = parser_modo_poc_ponto_a_ponto.add_subparsers(
        dest="papel"
    )

    subparsers_poc_ponto_a_ponto.add_parser(
        "produtor", help="iniciar poc com papel de produtor"
    )
    subparsers_poc_ponto_a_ponto.add_parser(
        "consumidor", help="iniciar poc com papel de consumidor"
    )

    if len(argumentos) == 0:
        argumentos = ["poc_ponto_a_ponto", "produtor"]
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
