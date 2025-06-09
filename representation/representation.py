# representation/representation.py

from abc import ABC, abstractmethod
from typing import Any

class Representation(ABC):
    """
    Interface abstrata para representações de grupos de simetria.
    Uma representação define operações como composição, inverso, e conjugação.
    """

    def __init__(self, nome_grupo: str):
        self.nome_grupo = nome_grupo

    @abstractmethod
    def adicionar(self, nome: str, dados: Any):
        """Adiciona uma operação representada sob o nome dado."""
        pass

    @abstractmethod
    def compor(self, a: Any, b: Any) -> Any:
        """Retorna a composição a ∘ b."""
        pass

    @abstractmethod
    def inverso(self, a: Any) -> Any:
        """Retorna o inverso de uma operação."""
        pass

    @abstractmethod
    def conjugar(self, a: Any, b: Any) -> Any:
        """Retorna a conjugação b⁻¹ a b."""
        pass

    @abstractmethod
    def nomes(self) -> list[str]:
        """Retorna os nomes das operações armazenadas."""
        pass

    @abstractmethod
    def valores(self) -> list[Any]:
        """Retorna os objetos das operações armazenadas."""
        pass

    @abstractmethod
    def aplicar(self, nome: str, vetor: list[float]) -> list[float]:
        """Aplica a operação de nome dado sobre um vetor."""
        pass

    @abstractmethod
    def __getitem__(self, nome: str) -> Any:
        """Permite acesso via representação[nome]."""
        pass