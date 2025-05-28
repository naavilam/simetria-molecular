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

from core.operation import Operation
import numpy as np

from permutation_tools import Permutation

class Permutations:
    def __init__(self, raw_dict):
        # raw_dict: dict[str, list[int]]
        self.nome_para_perm = {
            nome: Permutation(indices) for nome, indices in raw_dict.items()
        }

    def __getitem__(self, nome):
        return self.nome_para_perm[nome]

    def __len__(self):
        return len(self.nome_para_perm)

    def nomes(self):
        return list(self.nome_para_perm.keys())

    def valores(self):
        return list(self.nome_para_perm.values())

    def itens(self):
        return self.nome_para_perm.items()

    def __repr__(self):
        return f"Permutations({self.nome_para_perm})"

    def verificar_validade(self):
        for nome, perm in self.nome_para_perm.items():
            if not perm.is_valid():
                print(f"[AVISO] Permutação inválida: {nome} => {perm}")
                
# class Permutations(object):
#     """docstring for Permutations"""
    
#     def __init__(self, molecule, operacoes, tolerancia):
#         super(Permutations, self).__init__()
#         self.molecule = molecule
#         self.operacoes = operacoes 
#         self.tolerancia = tolerancia
        
#     def run_permutacoes(self):
#         permutacoes = {}
#         for op in self.operacoes:
#             mol_transformada = op.execute(self.molecule)
#             permutacao = self._obter_permutacao(self.molecule, mol_transformada)
#             print(permutacao)
#             permutacoes[op.nome] = permutacao
#         return permutacoes

#     def _obter_permutacao(self, orig_coords, transf_coords, tol=1e-3):
#         permutacao = []
#         for _, coord in transf_coords.como_tuplas():
#             for i, (_, ref) in enumerate(orig_coords.como_tuplas()):
#                 if np.allclose(coord, ref, atol=tol):
#                     permutacao.append(i + 1)
#                     break
#             else:
#                 permutacao.append(None)
#         return permutacao


