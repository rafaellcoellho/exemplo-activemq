from abc import ABC, abstractmethod

from gerenciador_activemq.dominio.recurso import NomeDoRecurso
from gerenciador_activemq.dominio.utilitarios import TipoDeRecurso


class OuvinteControladorRecurso(ABC):
    @abstractmethod
    def ao_adicionar_recurso(self, nome: NomeDoRecurso, tipo: TipoDeRecurso):
        raise NotImplementedError

    @abstractmethod
    def ao_remover_recurso(self, nome: NomeDoRecurso, tipo: TipoDeRecurso):
        raise NotImplementedError
