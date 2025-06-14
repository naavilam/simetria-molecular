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

from typing import Optional
from types import ClassMethodDescriptorType
from representation.representation_type import RepresentationType
from representation.representation_permutation import PermutationRepresentation
from representation.representation_matrix3d import Matrix3DRepresentation

from model.model_grupo import Group
from model.model_molecula import Molecule


class RepresentationBuilder:
    """
    Builder fluido para construção de representações a partir de um grupo e uma molécula.
    Permite selecionar o tipo e construir com simplicidade.
    """

    def __init__(self):
        self._group: Optional[Group] = None
        self._molecule: Optional[Molecule] = None
        self._tipo: RepresentationType = RepresentationType.PERMUTATION  # Default

    def de(self, group: Group, molecule: Molecule) -> 'RepresentationBuilder':
        self._group = group
        self._molecule = molecule
        return self

    def usar(self, tipo: RepresentationType) -> 'RepresentationBuilder':
        self._tipo = tipo
        return self

    def construir(self):
        """Summary

        Raises:
            ValueError: Description
        """
        if self._group is None or self._molecule is None:
            raise ValueError("RepresentationBuilder: 'group' e 'molecule' devem ser definidos antes de construir.")

        if self._tipo == RepresentationType.PERMUTATION:
            rep3d = Matrix3DRepresentation.from_group(self._group)
            return PermutationRepresentation.from_matrix3d(rep3d, self._molecule)
        elif self._tipo == RepresentationType.MATRIX_3D:
            return Matrix3DRepresentation.from_group(self._group)
        else:
            raise ValueError(f"Tipo de representação não suportado: {self._tipo}")