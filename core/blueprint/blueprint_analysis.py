from abc import ABC, abstractmethod
from typing import Tuple, List
from model.model_molecula import Molecule
from model.model_operacao_simetria import SymmetryOperation

class BlueprintAnalise(ABC):
    """
    Interface para análises que geram um Blueprint de Simetria.
    Responsável por transformar uma molécula em uma lista de operações de simetria
    + um resultado serializável (dict) para o sistema de resultados.
    """

    @abstractmethod
    def executar(self, molecule: Molecule) -> Tuple[dict, List[SymmetryOperation]]:
        """
        Executa a análise de blueprint sobre a molécula.

        Args:
            molecule (Molecule): A molécula a ser analisada.

        Returns:
            Tuple[dict, List[SymmetryOperation]]: - Um dicionário JSON-serializável contendo os resultados da análise (ex: nome do grupo, ordem, sistema, etc)
                - Uma lista de objetos SymmetryOperation representando as operações de simetria válidas para a molécula
        """
        pass