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
from representation.representation import Representation
from analysis.analise_grupo import AnaliseGrupo
from analysis.analise_permutacao import Permutacao
from analysis.analise_tabela_multiplicacao import TabelaMultiplicacao
from analysis.analise_classe_conjugacao import ClasseConjugacao
from analysis.analise_tabela_caracteres import TabelaCaracteres
from model.model_molecula import Molecule
from model.model_grupo import Group
from engine_analyzer.execution_strategy import calculate_score, select_strategy
from analysis.analise_tipo import AnaliseTipo
from typing import Optional

class SymmetryAnalyzer:

    """Summary
    """

    def __init__(self, molecule: Molecule):
        self.molecule = molecule
        self._symm_ops = None
        self._rep = None
        self._analises = {}
        self._resultados_pedidos = {}

    def set(self, analises: dict) -> 'SymmetryAnalyzer':
        """Recebe as flags de análises escolhidas pelo usuário e guarda internamente
        """
        self._analises = analises
        self._score = calculate_score(self._analises)

        return self

class SymmetryAnalyzer:



    def execute(self) -> dict:
        self._run_blueprint_phase()
        self._run_representation_phase()
        self._run_analysis_phase()
        return self._results

    def _run_blueprint_phase(self):
        blueprint_analyzer = AnaliseGrupo(SymmetryOperation)
        resultado, operacoes = blueprint_analyzer.executar(self.molecule)
        self._symm_ops = operacoes
        self._results['grupo'] = resultado

    def _run_representation_phase(self):
        self._rep = (
            RepresentationBuilder()
            .de_blueprint(self._symm_ops)
            .usar(RepresentationType.PERMUTATION)
            .construir()
        )

    def _run_analysis_phase(self):
        # Aqui pode até aplicar um Strategy
        for analise_tipo in self._analises_solicitadas:
            analise = AnaliseBuilder(analise_tipo, self._rep).build()
            resultado = analise.executar()
            self._results.update(resultado)

    def execute(self) -> dict:
        """Summary
        """
        strategy = select_strategy(self._score)

        return strategy.execute(self)

    def qual_grupo(self) -> 'SymmetryAnalyzer':
        self._analises[AnaliseTipo.GRUPO], self._symm_ops = AnaliseGrupo(self.molecule).executar()
        if AnaliseTipo.GRUPO in self._analises:
            self._resultados_pedidos[AnaliseTipo.GRUPO] = self._analises[AnaliseTipo.GRUPO]
        return self

    def permutacoes(self) -> 'SymmetryAnalyzer':
        self._analises[AnaliseTipo.PERMUTACOES] = Permutacao(self._symm_ops).executar()
        if AnaliseTipo.PERMUTACOES in self._analises:
            self._resultados_pedidos[AnaliseTipo.PERMUTACOES] = self._analises[AnaliseTipo.PERMUTACOES]
        return self

    def tabela_multiplicacao(self) -> 'SymmetryAnalyzer':
        self._analises[AnaliseTipo.TABELA_MULTIPLICACAO] = TabelaMultiplicacao(self._symm_ops).executar()
        if AnaliseTipo.TABELA_MULTIPLICACAO in self._analises:
            self._resultados_pedidos[AnaliseTipo.TABELA_MULTIPLICACAO] = self._analises[AnaliseTipo.TABELA_MULTIPLICACAO]
        return self

    def classes_conjugacao(self) -> 'SymmetryAnalyzer':
        """Summary
        """
        self._analises[AnaliseTipo.CLASSES_CONJUGACAO] = ClasseConjugacao(self._symm_ops).executar()
        if AnaliseTipo.CLASSES_CONJUGACAO in self._analises:
            self._resultados_pedidos[AnaliseTipo.CLASSES_CONJUGACAO] = self._analises[AnaliseTipo.CLASSES_CONJUGACAO]
        return self

    def tabela_caracteres(self) -> 'SymmetryAnalyzer':
        """Summary
        """
        self._analises[AnaliseTipo.TABELA_CARACTERES] = TabelaCaracteres(self._symm_ops).executar()
        if AnaliseTipo.TABELA_CARACTERES in self._analises:
            self._resultados_pedidos[AnaliseTipo.TABELA_CARACTERES] = self._analises[AnaliseTipo.TABELA_CARACTERES]
        return self

    def results(self) -> 'SymmetryAnalyzer':
        """Summary
        """
        return self

    def add_metadata(self) -> dict:
        """
        Adiciona metadados principais ao dicionário de resultados.
        Inclui informações sobre a molécula, grupo identificado, ordem, UUID, data e sistema cristalino.
        """

        grupo_resultado = self._analises.get(AnaliseTipo.GRUPO, {})
        nome_grupo = grupo_resultado.get("grupo", {}).get("nome", "Desconhecido")
        sistema_grupo = grupo_resultado.get("grupo", {}).get("sistema", "Desconhecido")
        ordem_grupo = len(grupo_resultado.get("operacoes", []))

        metadados = {
            "molecula": self.molecule.nome,
            "grupo": nome_grupo,
            "ordem": ordem_grupo,
            "uuid": self._uuid,
            "data": datetime.today().strftime("%Y-%m-%d %H:%M"),
            "sistema": sistema_grupo,
        }

        self._resultados_pedidos["metadados"] = metadados
        return self._resultados_pedidos