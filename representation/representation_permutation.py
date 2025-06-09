import numpy as np
from .representation import Representation
from.representation_matrix3d import Matrix3DRepresentation
from core.core_molecula import Molecule

class PermutationRepresentation(Representation):

    # @classmethod
    # def from_group(cls, group, molecule):
    #     inst = cls(group.nome)
    #     for op in group.operacoes:
    #         perm = cls._calcular_permutacao(molecule, op)
    #         inst.adicionar(op["nome"], perm)
    #     return inst

    @staticmethod
    def _calcular_permutacao(molecule, matriz_3x3, tolerancia=1e-3):
        coords_orig = np.array(molecule.coordenadas)
        elementos = molecule.elementos

        # Aplica a transformação: vetor' = matriz @ vetor
        coords_aplicadas = coords_orig @ matriz_3x3.T

        usados = set()
        permutacao = []

        for i, nova in enumerate(coords_aplicadas):
            especie = elementos[i]

            for j, antiga in enumerate(coords_orig):
                if j in usados:
                    continue
                if elementos[j] != especie:
                    continue
                if np.allclose(nova, antiga, atol=tolerancia):
                    permutacao.append(j)
                    usados.add(j)
                    break
            else:
                raise ValueError(f"Não foi possível mapear o átomo {i} ({especie}) após a operação.")

        return permutacao

    @classmethod
    def from_matrix3d(cls, rep3d: Matrix3DRepresentation, molecule: Molecule):
        inst = cls(rep3d.nome_grupo)
        for nome, matriz in rep3d:
            perm = cls._calcular_permutacao(molecule, matriz)
            inst.adicionar(nome, perm)
        return inst

    def get_permutacoes(self) -> dict:
        """
        Retorna o dicionário de permutações da representação.
        Cada entrada corresponde a uma operação e sua permutação associada.
        """
        return self._dados

    def __init__(self, nome_grupo: str):
        super().__init__(nome_grupo)
        self._dados = {}  # nome → permutação

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
        return self.compor(self.compor(inv_b, a), b)

    def nomes(self):
        return list(self._dados.keys())

    def valores(self):
        return list(self._dados.values())

    def __getitem__(self, nome):
        return self._dados[nome]