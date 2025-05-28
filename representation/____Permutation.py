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

from representation.representation_item_interface import RepresentationItem

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
