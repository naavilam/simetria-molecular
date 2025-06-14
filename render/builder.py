"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-06-14                                                                **
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

from .render_tipo import RenderTipo
from .render_tex import LatexReportGenerator
from .render_pdf import PdfReportGenerator
from .render_3D import MoleculeExplorer
from .render_gif import SimetriaAnimada
from .render import Renderer

class RendererBuilder:
    def __init__(self, formato: RenderTipo):
        self.formato = formato
        self._metadata = None
        self._molecule = None
        self._group = None

    def set(self, metadata: dict):
        self._metadata = metadata
        return self

    def to(self, molecule, group):
        self._molecule = molecule
        self._group = group
        return self

    def build(self) -> Renderer:
        if self.formato == RenderTipo.TEX:
            return LatexReportGenerator(self._metadata, self._molecule, self._group)
        elif self.formato == RenderTipo.PDF:
            return PdfReportGenerator(self._metadata, self._molecule, self._group)
        elif self.formato == RenderTipo.D3:
            return MoleculeExplorer(self._metadata, self._molecule, self._group)
        elif self.formato == RenderTipo.GIF:
            return SimetriaAnimada(self._metadata, self._molecule, self._group)
        else:
            raise ValueError(f"Formato de renderização não suportado: {self.formato}")