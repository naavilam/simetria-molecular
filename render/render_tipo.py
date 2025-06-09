from enum import Enum, auto

class RenderTipo(Enum):
    D3 = auto()
    GIF = auto()
    TEX = auto()
    PDF = auto()

    @classmethod
    def from_str(cls, valor: str):
        mapa = {
            "3d": cls.D3,
            "gif": cls.GIF,
            "tex": cls.TEX,
            "pdf": cls.PDF
        }
        try:
            return mapa[valor.lower()]
        except KeyError:
            raise ValueError(f"Tipo de renderização inválido: {valor}")