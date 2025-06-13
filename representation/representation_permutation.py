import numpy as np
from .representation import Representation
from.representation_matrix3d import Matrix3DRepresentation
from core.core_molecula import Molecule
from scipy.spatial.distance import cdist

class PermutationRepresentation(Representation):

    def __init__(self, nome_grupo: str):
        super().__init__(nome_grupo)
        self._dados = {}

    def calcular_permutacao_consistente(originais, transformadas, tolerancia=1e-2):
        """
        Retorna uma permutação consistente que associa cada coordenada transformada
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
            permutacao.append(melhor_indice)

        return permutacao

    @staticmethod
    def _calcular_permutacao(molecule, matriz, tolerancia=1e-2):
        coords_orig = np.array(molecule.coordenadas)
        coords_transf = np.dot(matriz, coords_orig.T).T

        dist = cdist(coords_transf, coords_orig)

        permutacao = [-1] * len(coords_orig)
        usados = set()

        for i in range(len(coords_transf)):
            # print(f"\n>>> Átomo {i} ({molecule.elementos[i]}) coordenada transformada: ")

            candidatos = []
            for j in range(len(coords_orig)):
                if j in usados:
                    continue
                if molecule.elementos[i] != molecule.elementos[j]:
                    continue
                dist_ij = dist[i, j]
                candidatos.append((j, dist_ij))
                # print(f"  - Distância até átomo {j} ({molecule.elementos[j]}): {dist_ij:.6f}")

            if not candidatos:
                raise ValueError(f"Não há mais candidatos válidos para mapeamento do átomo {i} ({molecule.elementos[i]}).")

            j_min, d_min = min(candidatos, key=lambda x: x[1])

            if d_min > tolerancia:
                # print(">>> Matriz aplicada:")
                # print(matriz)
                # print(">>> Candidatos válidos:")
                # print(candidatos)
                raise ValueError(f"Não foi possível mapear o átomo {i} ({molecule.elementos[i]}) após a operação.")

            permutacao[i] = j_min
            usados.add(j_min)

        return permutacao

    @classmethod
    def from_matrix3d(cls, rep3d: Matrix3DRepresentation, molecule: Molecule):
        inst = cls(rep3d.nome_grupo)
        for nome, matriz in rep3d:
            # print(f"\n>>> Aplicando operação: {nome}")
            perm = cls._calcular_permutacao(molecule, matriz)
            inst.adicionar(nome, perm)
        return inst

    def get_permutacoes(self) -> dict:
        """
        Retorna o dicionário de permutações da representação.
        Cada entrada corresponde a uma operação e sua permutação associada.
        """
        return self._dados

    def adicionar(self, nome: str, dados: list[int]):
        self._dados[nome] = dados

    def compor(self, a, b):
        return [b[a[i]] for i in range(len(a))]

    def inverso(self, a):
        inv = [0] * len(a)
        for i, val in enumerate(a):
            inv[val] = i
        return inv

    def aplicar(self, nome, vetor):
        perm = self._dados[nome]
        return [vetor[i] for i in perm]

    def conjugar(self, a, b):
        inv_b = self.inverso(b)
        return self.compor(self.compor(b, a), inv_b)

    def nomes(self):
        return list(self._dados.keys())

    def valores(self):
        return list(self._dados.values())

    def __getitem__(self, nome):
        return self._dados[nome]