"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-05-25                                                                **
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

import json
import re
import numpy as np
from pathlib import Path
from representation.representation import Representation
class ClasseConjugacao:
    def __init__(self, representation: Representation):
        self.rep = representation

    def gerar(self) -> tuple[dict, dict]:
        """
        Retorna uma tupla:
        - classes: dict com 'Classe 1': [nomes]
        - conjugacao_detalhada: dict com g -> h -> {resultado, detalhe}
        """
        nomes = self.rep.nomes()
        usados = set()
        conjugacy = []
        conjugacao_detalhada = {}

        for g in nomes:
            if g in usados:
                continue

            classe = set()
            conjugacao_detalhada[g] = {}

            for h in nomes:
                perm_g = self.rep[g]
                perm_h = self.rep[h]
                conj = self.rep.conjugar(perm_g, perm_h)

                # Encontrar qual nome corresponde ao resultado da conjugação
                for nome_k in nomes:
                    if self.rep[nome_k] == conj:
                        classe.add(nome_k)
                        conjugacao_detalhada[g][h] = {
                            "resultado": nome_k,
                            "detalhe": {
                                "g": perm_g,
                                "h": perm_h,
                                "hgh⁻¹": conj
                            }
                        }
                        break

            conjugacy.append(sorted(classe, key=nomes.index))
            usados.update(classe)

        # Formatando em forma de "Classe 1", "Classe 2", etc.
        classes_formatadas = {
            f"Classe {i+1}": classe for i, classe in enumerate(conjugacy)
        }

        return conjugacao_detalhada