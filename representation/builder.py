# representation/builder.py

from representation.representation_type import RepresentationType
from representation.representation_permutation import PermutationRepresentation
from representation.representation_matrix3d import Matrix3DRepresentation

from core.core_grupo import Group
from core.core_molecula import Molecule


class RepresentationBuilder:
    """
    Builder fluido para construção de representações a partir de um grupo e uma molécula.
    Permite selecionar o tipo e construir com simplicidade.
    """

    def __init__(self):
        self._group: Group = None
        self._molecule: Molecule = None
        self._tipo: RepresentationType = RepresentationType.PERMUTATION  # padrão

    def de(self, group: Group, molecule: Molecule):
        self._group = group
        self._molecule = molecule
        return self

    def usar(self, tipo: RepresentationType):
        self._tipo = tipo
        return self

    def construir(self):
        if self._tipo == RepresentationType.PERMUTATION:
            return PermutationRepresentation.from_group(self._group, self._molecule)
        elif self._tipo == RepresentationType.MATRIX_3D:
            return Matrix3DRepresentation.from_group(self._group)
        else:
            raise ValueError(f"Tipo de representação não suportado: {self._tipo}")