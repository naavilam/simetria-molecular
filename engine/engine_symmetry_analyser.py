"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-05-26                                                                **
**                                                      License: Custom Attribution License                                                       **
**                                                                                                                                                **
**                                                                      ---                                                                       **
**                                                                                                                                                **
**   Permission is granted to use, copy, modify, and distribute this file, provided that this notice is retained in full and that the origin of   **
**    the software is clearly and explicitly attributed to the original author. Such attribution must be preserved not only within the source     **
**       code, but also in any accompanying documentation, public display, distribution, or derived work, in both digital or printed form.        **
**                                                  For licensing inquiries: contact@chanah.dev                                                   **
====================================================================================================================================================
"""

# symmetry_analyzer.py
import numpy as np
from time import perf_counter
from analysis.analise_tabela_multiplicacao import TabelaMultiplicacao
from analysis.analise_classe_conjugacao import ClasseConjugacao
from core.core_molecula import Molecule
from render.render_tex import LatexReportGenerator
from render.render_3D import MoleculeExplorer
from render.render_pdf import PdfReportGenerator 
from render.render_tipo import RenderTipo
from representation.builder import RepresentationBuilder, RepresentationType
from representation.representation import Representation
from core.core_grupo import Group
from representation.builder import RepresentationBuilder, RepresentationType
from datetime import datetime
from analysis.analise_tipo import AnaliseTipo
from representation.representation_matrix3d import Matrix3DRepresentation
from representation.representation_permutation import PermutationRepresentation
from render.render import Renderer
from analysis.analise import analise

class SymmetryAnalyzer:

    def __init__(self, molecule, group, rep):
        self.molecule = molecule
        self.group = group
        self.rep = rep
        self._render = None
        self._analises = []
        self._uuid = None
        self._metadata = {}
        self._resultados = {}

    @classmethod
    def de(cls, group: Group, molecule: Molecule) -> 'SymmetryAnalyzer':
        rep = (
            RepresentationBuilder()
            .de(group, molecule)
            .usar(RepresentationType.PERMUTATION)
            .construir()
        )
        return cls(molecule, group, rep)

    def configurar(self, analises: list, render: RenderTipo, uuid: str) -> 'SymmetryAnalyzer':
        self._uuid = uuid
        self._metadata = self._gerar_metadata()
        self._analises = []

        for nome in analises:
            self._analises.append(analise(nome).from_rep(self.rep))

        self._render = get_renderer(render).set(self._metadata).to(self.molecule, self.group)
        return self

    def analisar(self) -> 'SymmetryAnalyzer':
        inicio = perf_counter()

        for analise in self._analises:
            self._resultados.update(analise.executar())

        self._resultados["tempo_execucao"] = f"{perf_counter() - inicio:.2f}s"
        return self

    def renderizar(self) -> str:

        return self._render.render(self._resultados)

    def _gerar_metadata(self) -> dict:
        return {
            "molecula": self.molecule.nome,
            "grupo": self.group.nome,
            "ordem": len(self.group.operacoes),
            "uuid": self._uuid,
            "data": datetime.today().strftime("%Y-%m-%d %H:%M"),
            "sistema": self.group.sistema
        }