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

from analysis.analise_tipo import AnaliseTipo
from representation.representation import Representation
from analysis.analise_tabela_multiplicacao import TabelaMultiplicacao
from analysis.analise_classe_conjugacao import ClasseConjugacao
from analysis.analise_tabela_caracteres import TabelaCaracteres
from analysis.analise_abeliano import Abeliano
from analysis.analise_ciclico import Ciclico
from analysis.analise_auto_valores import AutoValores
from analysis.analise_sub_grupos import SubGrupos
from analysis.analise_permutacao import Permutacao
from analysis.analise import Analise

class AnaliseBuilder:
    """
    Builder para instanciar a análise correta com base no tipo.
    """

    def __init__(self, tipo: AnaliseTipo, representacao: Representation):
        self.tipo = tipo
        self.representacao = representacao

    def build(self) -> Analise:
        """Summary

        Raises:
            ValueError: Description
        """
        if self.tipo == AnaliseTipo.TABELA_MULTIPLICACAO:
            return TabelaMultiplicacao(self.representacao)

        elif self.tipo == AnaliseTipo.CLASSES_CONJUGACAO:
            return ClasseConjugacao(self.representacao)

        elif self.tipo == AnaliseTipo.TABELA_CARACTERES:
            return TabelaCaracteres(self.representacao)

        elif self.tipo == AnaliseTipo.ABELIANO:
            return Abeliano(self.representacao)

        elif self.tipo == AnaliseTipo.CICLICO:
            return Ciclico(self.representacao)

        elif self.tipo == AnaliseTipo.AUTO_VALORES:
            return AutoValores(self.representacao)

        elif self.tipo == AnaliseTipo.SUB_GRUPOS:
            return SubGrupos(self.representacao)

        elif self.tipo == AnaliseTipo.PERMUTACOES:
            return Permutacao(self.representacao)

        else:
            raise ValueError(f"[AnaliseBuilder] Tipo de análise não suportado: {self.tipo}")