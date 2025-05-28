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
from representation.representation_item_interface import Representation
from representation.representation_type import RepresentationType
from enum import Enum

if TYPE_CHECKING:
    from core.group import Group
    from core.molecule import Molecule


class RepresentationStrategyBuilder(ABC):
    """Interface abstrata para estratégias de construção de representações."""
    
    @abstractmethod
    def construir(self, group: 'Group', molecule: 'Molecule') -> Representation:
        """Gera uma representação baseada no grupo e na molécula."""
        ...

class RepresentationStrategyBuilder:
    @staticmethod
    def get(tipo: RepresentationType):
        if tipo == RepresentationType.PERMUTATION:
            return PermutationRepresentationStrategy()
        elif tipo == RepresentationType.MATRIX_3D:
            return Matrix3DRepresentationStrategy()
        else:
            raise ValueError(f"Representação desconhecida: {tipo}")

class PermutationRepresentationStrategy(RepresentationStrategy):
    """Estratégia de construção de representação como permutações (1D)."""

    def construir(self, group: 'Group', molecule: 'Molecule') -> Representation:
        representation = Representation(group.nome)
        for operacao in group.operacoes:
            nome = operacao.nome
            matriz = operacao.matriz()
            mol_transformada = matriz @ molecule  # operador @ implementado na classe Molecule
            permutacao = Permutation.from_coords(molecule, mol_transformada, tol=group.tolerancia)
            representation.adicionar(nome, permutacao.indices)
        return representation


class Matrix3DRepresentationStrategy(RepresentationStrategy):
    """
    Implementa a estratégia de representação matricial 3D (rotacional) para cada operação do grupo.
    """
    def construir(self, group: 'GroupSymmetry', molecule: 'Molecule') -> Representation:
        representation = Representation(group.nome)
        for operacao in group.operacoes:
            nome = operacao.nome
            matriz = operacao.matriz()
            representation.adicionar(nome, matriz)
        return representation