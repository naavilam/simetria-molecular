from engine.representation import Representation
from engine.permutation_tools import Permutation
import numpy as np

class Representation(Implementation):
    """
    Gera a representação 1D (permutacional) de um grupo de simetria
    aplicada a uma molécula. Usa as operações 3D para transformar e comparar.
    """

    def __init__(self, group, molecule, tol=1e-3):
        self.group = group
        self.molecule = molecule
        self.tol = tol

    def construir(self):
        """
        Aplica cada operação do grupo à molécula e extrai a permutação resultante.
        
        Returns:
            Representation: objeto com dicionário nome → Permutation
        """
        rep = Representation(self.group.nome)

        for op in self.group.operacoes:
            nome = op.nome
            matriz = op.matriz()
            mol_transformada = self._aplicar_matriz(matriz)
            perm = Permutation.from_coords(self.molecule, mol_transformada, tol=self.tol)
            rep.adicionar(nome, perm)

        return rep

    def _aplicar_matriz(self, Rmat):
        """
        Aplica uma matriz de rotação/reflexão à molécula.
        """
        elementos = [el for el, _ in self.molecule.como_tuplas()]
        coords = [Rmat @ np.array(coord) for _, coord in self.molecule.como_tuplas()]

        nova = self.molecule.__class__.__new__(self.molecule.__class__)
        nova.elementos = elementos
        nova.coordenadas = coords
        return nova