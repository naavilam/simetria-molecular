"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-05-25                                                                **
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

import json
from pathlib import Path
from representation.representation import Representation
import numpy as np
from analysis.analise import Analise

class TabelaMultiplicacao(Analise):
    def __init__(self, representacao: Representation):
        """Summary
        """
        self.representacao = representacao
        self.operacoes = representacao.nomes()
        self.dados = self.gerar()

    @classmethod
    def from_rep(cls, rep: Representation) -> 'TabelaMultiplicacao':
        """Summary
        """
        return cls(rep)

    def executar(self) -> dict:
        """
        Gera a tabela de multiplicação: para cada par (A, B), calcula C = A * B
        tal que a operação composta tenha a mesma matriz (ou permutação) que C.

        Raises:
            ValueError: Description
        """
        tabela = {}
        for a in self.operacoes:
            linha = {}
            rep_a = self.representacao[a]
            for b in self.operacoes:
                rep_b = self.representacao[b]
                comp = self.representacao.compor(rep_a, rep_b)

                # Buscar nome do resultado da permutação composta
                nome_resultado = None
                for c in self.operacoes:
                    if np.allclose(self.representacao[c], comp):
                        nome_resultado = c
                        break

                if nome_resultado is None:
                    raise ValueError(f"Composição {a} * {b} não encontrada.")

                linha[b] = {
                    "nome": nome_resultado,
                    "permutacao_op1": rep_a,
                    "permutacao_op2": rep_b,
                    "permutacao_resultante": comp
                }

            tabela[a] = linha
        return tabela
