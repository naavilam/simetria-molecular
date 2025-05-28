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
from analysis.tabela_multiplicacao import TabelaMultiplicacao
from analysis.classe_conjugacao import ClasseConjugacao
from analysis.permutations import Permutations
from core.molecule import Molecule
from core.operation import Operation
from render.latex import LatexReportGenerator
from render.pyvista import PyvistaVisualizer
from representation.representation_strategy_builder import RepresentationStrategyBuilder,RepresentationType 

from representations.strategy_builder import RepresentationStrategyBuilder, RepresentationType
from representations.representation import Representation
from group import Group
from molecule import Molecule

class SymmetryAnalyzer:

    def __init__(self, molecule, group):
        self.molecule = molecule
        self.group = group
        self.transformacoes = ()
        self.multiplication_table = ()
        self.conjugacy_classes = ()
        self.character_table = ()

    @classmethod
    def de(cls, group: Group, molecule: Molecule) -> 'SymmetryAnalyzer':
        return cls(group, molecule)

    def usar(self, tipo: RepresentationType) -> 'SymmetryAnalyzer':
        self.strategy = RepresentationStrategyBuilder.get(tipo)
        return self

    def get(self) -> Representation:
        if not self.strategy:
            raise ValueError("É preciso escolher uma estratégia de representação com `.usar()` antes de chamar `.get()`.")
        return self.strategy.construir(self.group, self.molecule)

    def run_analysis(self, molecule, group):
        inicio = perf_counter()

        strategy = RepresentationStrategyBuilder.get(RepresentationType.PERMUTATION)
        representation = strategy.construir(group, molecule)
        # suponha que você já criou a representação usando a estratégia
        representation = strategy.construir(grupo, molecula)

        # tabela de multiplicação
        tabela = MultiplicationTable(representation).gerar()

        # classes de conjugação
        classes = ConjugacyClass(representation, tabela).gerar()
        

        # permutacoes = Permutations(self.molecule, self.group.operacoes, self.group.tolerancia).run_permutacoes()
        # print(permutacoes)
        # tab_mult = TabelaMultiplicacao(permutacoes).gerar()
        # class_conj = ClasseConjugacao(permutacoes, tab_mult).gerar_classe_conjugacao()

        tempo = perf_counter() - inicio

        return {
            "permutacoes": permutacoes,
            "tabela": tab_mult,
            "classes": class_conj,
            "tempo_execucao": f"{tempo:.2f}s"
        }

    def render(self, formato="latex") -> str:
        if formato == "latex":
            return LatexRenderer().render(self)
        elif formato == "text":
            return TextRenderer().render(self)
        ...
    def render_operation(self, selected_op):
        pyvis = PyvistaVisualizer()
