from dataclasses import dataclass


@dataclass
class InformacaoRecurso:
    nome: str
    quantidade_de_mensagens: int
