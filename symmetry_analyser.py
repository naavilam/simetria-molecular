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

from representation.builder import RepresentationBuilder, RepresentationType
from analysis.analise_grupo import AnaliseGrupo
from analysis.analise_permutacao import Permutacao
from analysis.analise_tabela_multiplicacao import TabelaMultiplicacao
from analysis.analise_classe_conjugacao import ClasseConjugacao
from analysis.analise_tabela_caracteres import TabelaCaracteres
from core.core_molecula import Molecule
from core.core_grupo import Group
from engine.execution_strategy import calculate_score, select_strategy
from analysis.analise_tipo import AnaliseTipo

class SymmetryAnalyzer:

    """Summary
    """

    def __init__(self, molecule: Molecule):
        """Summary
        """
        self.molecule = molecule
        self._analise_flags = []

    def set(self, analises_flags: dict) -> 'SymmetryAnalyzer':
        """Recebe as flags de análises escolhidas pelo usuário e guarda internamente
        """
        self._analises_flags = analises_flags
        self._score = calculate_score(self._analises_flags)

        return self

    def execute(self) -> dict:
        """Summary
        """
        strategy = select_strategy(self._score)

        return strategy.execute()

    def qual_grupo(self) -> 'SymmetryAnalyzer':
        """Summary
        """
        self._analise_grupo_resultados = AnaliseGrupo(self.rep).executar()
        if AnaliseTipo.GRUPO in self._analises_flags:
            self._resultados_pedidos.update(self._analise_grupo_resultados)
        return self

    def permutacoes(self) -> 'SymmetryAnalyzer':
        self._analise_permutacoes_resultados = Permutacao(self.rep).executar()
        if AnaliseTipo.PERMUTACOES in self._analises_flags:
            self._resultados_pedidos.update(self._analise_permutacoes_resultados)
        return self

    def tabela_multiplicacao(self) -> 'SymmetryAnalyzer':
        self._analise_multiplicacao_resultados = TabelaMultiplicacao(self.rep).executar()
        if AnaliseTipo.TABELA_MULTIPLICACAO in self._analises_flags:
            self._resultados_pedidos.update(self._analise_multiplicacao_resultados)
        return self

    def classes_conjugacao(self) -> 'SymmetryAnalyzer':
        self._analise_classes_resultados = ClasseConjugacao(self.rep).executar()
        if AnaliseTipo.TABELA_MULTIPLICACAO in self._analises_flags:
            self._resultados_pedidos.update(self._analise_classes_resultados)
        return self

    def tabela_caracteres(self) -> 'SymmetryAnalyzer':
        """Summary
        """
        self._analise_caracteres_resultados = TabelaCaracteres(self.rep).executar()
        if AnaliseTipo.TABELA_CARACTERES in self._analises_flags:
            self._resultados_pedidos.update(self._analise_caracteres_resultados)
        return self

    def results(self) -> dict:
        return self._resultados_pedidos