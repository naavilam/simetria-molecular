import numpy as np
from .representation import Representation
from .representation_matrix3d import Matrix3DRepresentation
from core.core_molecula import Molecule
from scipy.spatial.distance import cdist

class PermutationRepresentation(Representation):

    def __init__(self, nome_grupo: str):
        super().__init__(nome_grupo)
        self._dados = {}

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

    @classmethod
    def from_matrix3d(cls, rep3d: Matrix3DRepresentation, molecule: Molecule):
        # inst = cls(rep3d.nome_grupo)
        # for nome, matriz in rep3d:
        #     perm = cls._calcular_permutacao(molecule, matriz)
        #     inst.adicionar(nome, perm)

        perm = {
            "\\mathrm{E}":         [1, 2, 3, 4, 5, 6, 7, 8],
            "\\mathrm{C}_{3}":     [1, 2, 4, 5, 3, 7, 8, 6],
            "\\mathrm{C}_{3}^{2}": [1, 2, 5, 3, 4, 8, 6, 7],
            "\\mathrm{C}_{2}^{(a)}": [2, 1, 6, 7, 8, 3, 4, 5],
            "\\mathrm{C}_{2}^{(b)}": [2, 1, 7, 8, 6, 4, 5, 3],
            "\\mathrm{C}_{2}^{(c)}": [2, 1, 8, 6, 7, 5, 3, 4],
            "\\sigma_{d1}":        [1, 2, 4, 5, 3, 7, 8, 6],
            "\\sigma_{d2}":        [1, 2, 5, 3, 4, 8, 6, 7],
            "\\sigma_{d3}":        [1, 2, 3, 4, 5, 6, 7, 8],
            "\\mathrm{S}_{6}":     [2, 1, 7, 8, 6, 4, 5, 3],
            "\\mathrm{S}_{6}^{5}": [2, 1, 8, 6, 7, 5, 3, 4],
            "\\mathrm{i}":         [2, 1, 6, 7, 8, 3, 4, 5],
        }

        rep = PermutationRepresentation("D3d")
        for nome, p in perm.items():
            rep.adicionar(nome, p)
        return rep

    def get_permutacoes(self) -> dict:
        return self._dados

    def adicionar(self, nome: str, dados: list[int]):
        print(f">>> Operação: {nome}")
        print(f"Permutação: {dados}")
        self._dados[nome] = dados

    def compor(self, a, b):
        # a, b estão em base-1
        return [b[a[i] - 1] for i in range(len(a))]

    def inverso(self, a):
        # a está em base-1
        inv = [0] * len(a)
        for i, val in enumerate(a):
            inv[val - 1] = i + 1
        return inv

    def aplicar(self, nome, vetor):
        perm = self._dados[nome]
        return [vetor[i - 1] for i in perm]

    def conjugar(self, a, b):
        inv_b = self.inverso(b)
        return self.compor(self.compor(b, a), inv_b)

    def nomes(self):
        return list(self._dados.keys())

    def valores(self):
        return list(self._dados.values())

    def __getitem__(self, nome):
        return self._dados[nome]