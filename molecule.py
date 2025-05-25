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

import numpy as np

class Molecule:

    """Summary
    """
    
    def __init__(self, path_arquivo_xyz):
        """Summary
        """
        self.path = path_arquivo_xyz
        self.elementos = []
        self.coordenadas = []
        self._carregar()

    def _carregar(self):
        """Summary
        """
        with open(self.path, 'r') as f:
            linhas = f.readlines()

        natomos = int(linhas[0])
        dados = linhas[2:2 + natomos]

        self.elementos = []
        self.coordenadas = []

        for linha in dados:
            partes = linha.split()
            elemento = partes[0]
            coords = np.array(list(map(float, partes[1:4])))
            self.elementos.append(elemento)
            self.coordenadas.append(coords)

    def como_tuplas(self):
        return list(zip(self.elementos, self.coordenadas))

    def __len__(self):
        return len(self.elementos)