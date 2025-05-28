from enum import Enum

class RepresentationType(Enum):
    """Tipos de representação do grupo de simetria"""
    
    PERMUTATION = "permutation"
    MATRIX_3D = "3d"

    @classmethod
    def from_str(cls, valor: str):
        mapa = {
            "permutation": cls.PERMUTATION,
            "perm": cls.PERMUTATION,
            "1d": cls.PERMUTATION,
            "3d": cls.MATRIX_3D,
            "matrix": cls.MATRIX_3D,
            "matriz": cls.MATRIX_3D
        }
        try:
            return mapa[valor.lower()]
        except KeyError:
            raise ValueError(f"Tipo de representação inválido: {valor}")