"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-06-14                                                                **
**                                                      License: Custom Attribution License                                                       **
**                                                                                                                                                **
**    Este módulo faz parte do projeto de simetria molecular desenvolvido no contexto da disciplina de pós-graduação PGF5261 Teoria de Grupos     **
**                                                       Aplicada para Sólidos e Moléculas.                                                       **
**                                                                                                                                                **
**   Permission is granted to use, copy, modify, and distribute this file, provided that this notice is retained in full and that the origin of   **
**    the software is clearly and explicitly attributed to the original author. Such attribution must be preserved not only within the source     **
**       code, but also in any accompanying documentation, public display, distribution, or derived work, in both digital or printed form.        **
**                                                  For licensing inquiries: contact@chanah.dev                                                   **
====================================================================================================================================================
"""

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