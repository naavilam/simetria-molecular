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
from render.render_3D import PyvistaVisualizer
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

class SymmetryAnalyzer:

    def __init__(self, molecule, group):
        self.molecule = molecule
        self.group = group
        self._tipo = RepresentationType.PERMUTATION  # padrão
        self._analises = []
        self._resultado = None
        self._uuid = None

    @classmethod
    def de(cls, group: Group, molecule: Molecule) -> 'SymmetryAnalyzer':
        return cls(molecule, group)

    def usar(self, tipo: RepresentationType)-> 'SymmetryAnalyzer':
        if tipo == RepresentationType.MATRIX_3D:
            self.rep = Matrix3DRepresentation.from_group(self.group)

        elif tipo == RepresentationType.PERMUTATION:
            rep3d = Matrix3DRepresentation.from_group(self.group)
            self.rep = PermutationRepresentation.from_matrix3d(rep3d, self.molecule)

        else:
            raise ValueError(f"Tipo de representação não suportado: {tipo}")

        self._tipo = tipo
        return self

    def configurar(self, analises: list, uuid: str) -> 'SymmetryAnalyzer':
        self._analises = analises
        self._uuid = uuid
        return self

    def get_representacao(self) -> Representation:
        return (
            RepresentationBuilder()
            .de(group=self.group, molecule=self.molecule)
            .usar(self._tipo)
            .construir()
        )

    def executar(self) -> 'SymmetryAnalyzer':
        inicio = perf_counter()
        representacao = self.get_representacao()

        resultado = {}
        if AnaliseTipo.PERMUTACOES in self._analises:
            resultado["permutacoes"] = representacao.get_permutacoes()

        if AnaliseTipo.TABELA_MULTIPLICACAO in self._analises:
            resultado["tabela"] = TabelaMultiplicacao(representacao).gerar()

        if AnaliseTipo.CLASSES_CONJUGACAO in self._analises:
            resultado["classes"] = ClasseConjugacao(representacao, resultado["tabela"]).gerar()

        resultado["tempo_execucao"] = f"{perf_counter() - inicio:.2f}s"
        self._resultado = resultado
        return self

    def renderizar(self, formato: RenderTipo) -> str:
        if self._resultado is None:
            raise RuntimeError("Você precisa chamar `.executar()` antes de `.renderizar()`.")

        metadata = self._gerar_metadata()
        if formato == RenderTipo.TEX:
            return LatexReportGenerator(metadata, self._resultado).gerar_documento()
        elif formato == RenderTipo.PDF:
            return PdfReportGenerator(metadata, self._resultado).gerar_pdf()
        else:
            raise ValueError(f"Formato de saída não suportado: {formato}")

    def _gerar_metadata(self) -> dict:
        return {
            "molecula": self.molecule.nome,
            "grupo": self.group.nome,
            "ordem": len(self.group.operacoes),
            "uuid": self._uuid,
            "data": datetime.today().strftime("%Y-%m-%d %H:%M"),
            "sistema": self.group.sistema
        }

    def renderizar_operacao(self, selected_op):
        return PyvistaVisualizer().render(selected_op, self.molecule, self.group)