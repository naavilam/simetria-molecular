from .render_3D import MoleculeExplorer
from .render_gif import SimetriaAnimada
from .render_pdf import PdfReportGenerator
from .render_tex import LatexReportGenerator
from .RenderTipo import RenderTipo  # Enum dos formatos de saída

class Factory(object):
    """docstring for RendererBuilder"""
    def __init__(self, arg):
        super(Factory, self).__init__()
        self.arg = arg

def get_renderer(formato: RenderTipo, metadata, resultado, molecula, grupo) -> Renderer:
    if formato == RenderTipo.TEX:
        return LatexReportGenerator(metadata, resultado)
    elif formato == RenderTipo.PDF:
        return PdfReportGenerator(metadata, resultado)
    elif formato == RenderTipo.D3:
        return MoleculeExplorer(metadata, molecula, grupo)
    else:
        raise ValueError(f"Formato de saída não suportado: {formato}")