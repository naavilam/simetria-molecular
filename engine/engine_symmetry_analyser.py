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

class SymmetryAnalyzer:

    def __init__(self, molecule, group):
        self.molecule = molecule
        self.group = group
        self._tipo = RepresentationType.PERMUTATION  # padrão

    @classmethod
    def de(cls, group: Group, molecule: Molecule) -> 'SymmetryAnalyzer':
        return cls(molecule, group)

    def usar(self, tipo: RepresentationType) -> 'SymmetryAnalyzer':
        self._tipo = tipo
        return self

    def get_representacao(self):
        return (
            RepresentationBuilder()
            .de(group=self.group, molecule=self.molecule)
            .usar(self._tipo)
            .construir()
        )

    def run_analysis(self):
        from time import perf_counter
        inicio = perf_counter()

        representacao = self.get_representacao()

        # Aqui você executa os blocos ativos com base na representação:
        permutacoes = representacao.get_permutacoes()  # hipotético
        tab_mult = TabelaMultiplicacao(permutacoes).gerar()
        class_conj = ClasseConjugacao(permutacoes, tab_mult).gerar_classe_conjugacao()

        tempo = perf_counter() - inicio

        return {
            "permutacoes": permutacoes,
            "tabela": tab_mult,
            "classes": class_conj,
            "tempo_execucao": f"{tempo:.2f}s"
        }

    def render(self, formato: RenderTipo = RenderTipo.TEX, uuid=None) -> str:
        if formato == RenderTipo.TEX:
            metadata = self._gerar_metadata(self.molecule, self.group, uuid)
            return LatexReportGenerator().render(self)
        elif formato == RenderTipo.PDF:
            return PdfReportGenerator().render(self)
        else:
            raise ValueError(f"Formato de saída não suportado: {formato}")

    def _gerar_metadata(self, molecula, grupo, uuid) -> dict:
        print(">>>>>>>>>>>>>>>")
        print(grupo)
        print(type(grupo))
        return {
            "molecula": molecula.nome,
            "grupo": grupo.nome,
            "ordem": len(grupo.operacoes),
            "uuid": uuid,
            "data": datetime.today().strftime("%Y-%m-%d %H:%M"),
            "sistema": grupo.sistema
        }

    def render_operation(self, selected_op):
        pyvis = PyvistaVisualizer()
        return pyvis.render(selected_op, self.molecule, self.group)
