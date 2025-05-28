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
from typing import TYPE_CHECKING
from representation.representation_interface import Representation
from representation.representation_type import RepresentationType
from enum import Enum

if TYPE_CHECKING:
    from core.core_grupo import Group
    from core.core_molecula import Molecule


class RepresentationStrategyBuilder(ABC):
    """Interface abstrata para estratégias de construção de representações."""
    
    @abstractmethod
    def construir(self, group: 'Group', molecule: 'Molecule') -> Representation:
        """Gera uma representação baseada no grupo e na molécula."""
        ...

    @staticmethod
    def get(tipo: RepresentationType):
        if tipo == RepresentationType.PERMUTATION:
            return PermutationRepresentationStrategy()
        elif tipo == RepresentationType.MATRIX_3D:
            return Matrix3DRepresentationStrategy()
        else:
            raise ValueError(f"Representação desconhecida: {tipo}")



