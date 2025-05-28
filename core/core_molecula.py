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

from types import ClassMethodDescriptorType
import numpy as np

class Molecule:

    """Summary
    """
    
    def __init__(self, nome, elementos, coordenadas):
        """Summary
        """
        self.nome = nome
        self.elementos = elementos
        self.coordenadas = coordenadas

    @classmethod
    def from_file(cls, path_file):
        with open(path_file, 'r') as f:
            linhas = f.readlines()
        nome, elementos, coordenadas = cls._carregar(linhas)
        return cls(nome, elementos, coordenadas)

    @classmethod
    def _carregar(cls, linhas):
        """Summary
        """
        natomos = int(linhas[0])
        nome = linhas[1]
        dados = linhas[2:2 + natomos]

        elementos = []
        coordenadas = []

        for linha in dados:
            partes = linha.split()
            elemento = partes[0]
            coords = np.array(list(map(float, partes[1:4])))
            elementos.append(elemento)
            coordenadas.append(coords)
        return nome, elementos, coordenadas

    def como_tuplas(self):
        return list(zip(self.elementos, self.coordenadas))

    def __len__(self):
        return len(self.elementos)