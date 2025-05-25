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

import numpy as np
from gera_permutacoes import detalhe_operacao, aplicar_matriz
from gera_tabela_multiplicacao import gerar_tabela_multiplicacao
from gera_classes_conjugacao import gerar_classe_conjugacao


class SimetriaMolecular:

    """Description
    
    Attributes:
        mol (TYPE): Description
        operacoes (TYPE): Description
        permutacoes (dict): Description
    """
    
    def __init__(self, mol, operacoes):
        self.mol = mol
        self.operacoes = operacoes
        self.permutacoes = {}

    def analisar(self):
        """Executa a análise de simetria e imprime os resultados.
        """
        for idx, op in enumerate(self.operacoes, start=1):
            desc = op.get("comentario", f"operação {idx}")
            print(f"[{idx}] {desc}")
            Rmat, destaque = detalhe_operacao(op)
            mol_transformada = aplicar_matriz(self.mol, Rmat)
            permutacao = self.obter_permutacao(self.mol, mol_transformada)
            self.permutacoes[op["nome"]] = permutacao

        print("*****************Operações Básicas*****************")
        for nome, perm in self.permutacoes.items():
            print(f"{nome}: {perm}")
        print("********Fim da Analise das Operações Básicas*******")

        tab_mult = gerar_tabela_multiplicacao(self.permutacoes)
        gerar_classe_conjugacao(self.permutacoes, tab_mult)

    @staticmethod
    def obter_permutacao(orig_coords, transf_coords, tol=1e-3):
        """Compara coordenadas para identificar a permutação resultante.
        
        Args:
            orig_coords (list): Lista de coordenadas originais.
            transf_coords (list): Lista de coordenadas transformadas.
            tol (float): Tolerância para comparacão de similaridade.
        
        Returns:
            list: Permutação dos índices.
        """
        permutacao = []
        for _, coord in transf_coords:
            for i, (_, ref) in enumerate(orig_coords):
                if np.allclose(coord, ref, atol=tol):
                    permutacao.append(i)
                    break
            else:
                permutacao.append(None)
        return permutacao