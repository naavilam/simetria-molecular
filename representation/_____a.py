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

# ---------------------------------------------------------------------
# Interface de Item de Representação (Contrato de permutação, matriz, etc)
# ---------------------------------------------------------------------
class RepresentationItem(ABC):
    @abstractmethod
    def compose(self, other: "RepresentationItem") -> "RepresentationItem":
        pass

    @abstractmethod
    def inverse(self) -> "RepresentationItem":
        pass

    @abstractmethod
    def equals(self, other: "RepresentationItem") -> bool:
        pass

# ---------------------------------------------------------------------
# Implementação concreta: Permutação
# ---------------------------------------------------------------------
class Permutation(RepresentationItem):
    def __init__(self, indices: list[int]):
        self.indices = indices

    def compose(self, other: "Permutation") -> "Permutation":
        return Permutation([self.indices[i] for i in other.indices])

    def inverse(self) -> "Permutation":
        inversa = [0] * len(self.indices)
        for i, j in enumerate(self.indices):
            inversa[j] = i
        return Permutation(inversa)

    def equals(self, other: "Permutation") -> bool:
        return self.indices == other.indices

    def __repr__(self):
        return f"Permutation({self.indices})"

# ---------------------------------------------------------------------
# Interface para estratégias de representação
# ---------------------------------------------------------------------
class RepresentationStrategy(Protocol):
    def build(self, molecule, group) -> Dict[str, RepresentationItem]:
        ...

# ---------------------------------------------------------------------
# Estratégia: Representação como Permutação
# ---------------------------------------------------------------------
class PermutationRepresentationStrategy:
    def build(self, molecule, group) -> Dict[str, RepresentationItem]:
        representation = {}
        for op in group.operacoes:
            Rmat, _ = group.detalhe_operacao(op)
            mol_transformada = self._aplicar_matriz(molecule, Rmat)
            perm = self._obter_permutacao(molecule, mol_transformada)
            representation[op["nome"]] = Permutation(perm)
        return representation

    def _aplicar_matriz(self, molecule, Rmat):
        elementos = [el for el, _ in molecule.como_tuplas()]
        coords = [Rmat @ coord for _, coord in molecule.como_tuplas()]
        nova = molecule.__class__.__new__(molecule.__class__)
        nova.elementos = elementos
        nova.coordenadas = coords
        return nova

    def _obter_permutacao(self, orig_coords, transf_coords, tol=1e-3):
        permutacao = []
        for _, coord in transf_coords.como_tuplas():
            for i, (_, ref) in enumerate(orig_coords.como_tuplas()):
                if all(abs(coord[j] - ref[j]) < tol for j in range(3)):
                    permutacao.append(i)
                    break
            else:
                permutacao.append(None)
        return permutacao