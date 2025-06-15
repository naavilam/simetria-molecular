"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-06-15                                                                **
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

    @staticmethod
    def calcular_permutacao_consistente(originais, transformadas, tolerancia=1e-2):
        """
        Retorna uma permutação (base-1) que associa cada coordenada transformada
        a uma coordenada original, sem repetições, com base em distância mínima dentro da tolerância.
        """
        n = len(originais)
        usados = set()
        permutacao = []

        for i, r_t in enumerate(transformadas):
            melhor_indice = None
            melhor_dist = None

            for j, r_o in enumerate(originais):
                if j in usados:
                    continue
                dist = np.linalg.norm(np.array(r_t) - np.array(r_o))
                if dist <= tolerancia:
                    if melhor_dist is None or dist < melhor_dist or (np.isclose(dist, melhor_dist) and j < melhor_indice):
                        melhor_dist = dist
                        melhor_indice = j

            if melhor_indice is None:
                raise ValueError(f"Não foi possível associar a coordenada transformada {i} a nenhuma original dentro da tolerância.")

            usados.add(melhor_indice)
            permutacao.append(melhor_indice + 1)  # ⬅️ Corrigido para base-1

        return permutacao

    @staticmethod
    def _calcular_permutacao(molecule, matriz, tolerancia=1e-2):
        """Summary

        Raises:
            ValueError: Description
        """
        coords_orig = np.array(molecule.coordenadas)
        coords_transf = np.dot(matriz, coords_orig.T).T

        dist = cdist(coords_transf, coords_orig)

        permutacao = [-1] * len(coords_orig)
        usados = set()

        for i in range(len(coords_transf)):
            candidatos = []
            for j in range(len(coords_orig)):
                if j in usados:
                    continue
                if molecule.elementos[i] != molecule.elementos[j]:
                    continue
                dist_ij = dist[i, j]
                candidatos.append((j, dist_ij))

            if not candidatos:
                raise ValueError(f"Não há mais candidatos válidos para o átomo {i} ({molecule.elementos[i]}).")

            j_min, d_min = min(candidatos, key=lambda x: x[1])

            if d_min > tolerancia:
                raise ValueError(f"Não foi possível mapear o átomo {i} ({molecule.elementos[i]}) após a operação.")

            permutacao[i] = j_min + 1  # ⬅️ Corrigido para base-1
            usados.add(j_min)

        return permutacao


    def compor(self, a, b):
        # a, b estão em base-1
        return [b[a[i] - 1] for i in range(len(a))]

    def inverso(self, a):
        """Summary
        """
        # a está em base-1
        inv = [0] * len(a)
        for i, val in enumerate(a):
            inv[val - 1] = i + 1
        return inv

    def conjugar(self, a, b):
        inv_b = self.inverso(b)
        return self.compor(self.compor(b, a), inv_b)