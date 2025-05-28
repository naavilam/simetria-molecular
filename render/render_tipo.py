from enum import Enum, auto

class RenderTipo(Enum):
    D3 = auto()
    GIF = auto()
    LATEX = auto()
    TEXTO = auto()

    @classmethod
    def from_str(cls, valor: str):
        mapa = {
            "3d": cls.D3,
            "gif": cls.GIF,
            "latex": cls.LATEX,
            "txt": cls.TEXTO,
            "texto": cls.TEXTO
        }
        try:
            return mapa[valor.lower()]
        except KeyError:
            raise ValueError(f"Tipo de renderização inválido: {valor}")