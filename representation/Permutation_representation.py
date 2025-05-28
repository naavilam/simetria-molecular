"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-05-27                                                                **
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
from typing import Dict, Protocol
    
class Representation:
    """
    Armazena uma representação de grupo de simetria, seja ela
    uma lista de permutações, matrizes ou qualquer forma estruturada.
    """

    def compose(self, nome_a: str, nome_b: str):
        a = self._dados[nome_a]
        b = self._dados[nome_b]
        if hasattr(a, 'compose'):
            return a.compose(b)
        else:
            return a @ b

    def inverse(self, nome: str):
        a = self._dados[nome]
        if hasattr(a, 'inverse'):
            return a.inverse()
        else:
            from numpy.linalg import inv
            return inv(a)

    def is_equal(self, a_repr, b_repr) -> bool:
        if hasattr(a_repr, 'equals'):
            return a_repr.equals(b_repr)
        else:
            import numpy as np
            return np.allclose(a_repr, b_repr)

    def conjugate(self, nome_a: str, nome_b: str):
        """Conjuga a por b: b⁻¹ a b"""
        a = self._dados[nome_a]
        b = self._dados[nome_b]
        b_inv = self.inverse(nome_b)

        if hasattr(a, 'compose') and hasattr(b_inv, 'compose'):
            return b_inv.compose(a).compose(b)
        else:
            return b_inv @ a @ b