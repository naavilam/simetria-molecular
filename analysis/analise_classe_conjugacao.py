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
import re
import numpy as np
from pathlib import Path
from representation.representation import Representation

# conjugacy_class.py

class ClasseConjugacao:
    def __init__(self, representation: Representation, mult_table: dict):
        self.rep = representation
        self.tab = mult_table

    def gerar(self) -> dict:
        conjugacy = {}
        nomes = self.rep.nomes_operacoes()
        for g in nomes:
            classe = set()
            for h in nomes:
                inv_h = self.rep[h].inverse() if hasattr(self.rep[h], 'inverse') else np.linalg.inv(self.rep[h])
                conj = self.rep[h] @ self.rep[g] @ inv_h
                for nome_k, op_k in self.rep:
                    if np.allclose(conj, op_k):
                        classe.add(nome_k)
                        break
            conjugacy[g] = sorted(list(classe))
        return conjugacy

# from permutation_tools import Permutation

# class ClasseConjugacao:
#     def __init__(self, permutacoes, tabela_multiplicacao):
#         self.permutacoes = permutacoes  # instancia de Permutations
#         self.tab_mult = tabela_multiplicacao  # opcional

#     def gerar_classe_conjugacao(self):
#         nomes = self.permutacoes.nomes()
#         classes = []
#         vistos = set()

#         for nome in nomes:
#             if nome in vistos:
#                 continue
#             classe = set()
#             p = self.permutacoes[nome]
#             for nome2 in nomes:
#                 p2 = self.permutacoes[nome2]
#                 conj = p2.inverse().compose(p).compose(p2)
#                 for nome_ref, p_ref in self.permutacoes.itens():
#                     if conj == p_ref:
#                         classe.add(nome_ref)
#                         break
#             classes.append(sorted(classe))
#             vistos.update(classe)

#         return self._formatar_latex(classes)

#     def _formatar_latex(self, classes):
#         latex = ["\\begin{array}{l}"]
#         for i, classe in enumerate(classes):
#             latex.append(f"\\mathcal{{C}}_{{{i+1}}} = \\{{ " + ", ".join(classe) + " \\}} \\\\")
#         latex.append("\\end{array}")
#         return "\n".join(latex)

# class ClasseConjugacao:

#     """Summary
#     """
    
#     def __init__(self, permutacoes, tabela_mult):
#         """Summary
#         """
#         self.permutacoes = permutacoes
#         self.tabela_mult = tabela_mult


#     def gerar_classe_conjugacao(self):

#         nomes = list(self.permutacoes.keys())
#         perms = list(self.permutacoes.values())
#         nome_por_perm = {tuple(p): nome for nome, p in self.permutacoes.items()}

#         classes = {}
#         for i, nome_i in enumerate(nomes):
#             pi = perms[i]
#             conj_class = set()
#             for j, nome_j in enumerate(nomes):
#                 pj = perms[j]
#                 pj_inv = [pj.index(k+1) for k in range(len(pj))]
#                 comp1 = self._compor(pj, pi)
#                 conj = self._compor(comp1, pj_inv)
#                 nome_conjugado = nome_por_perm.get(tuple(conj))
#                 if nome_conjugado:
#                     conj_class.add(nome_conjugado)
#             classes[nome_i] = conj_class

#         self.salvar_classes_conjugacao(classes)
#         self.gerar_operacoes_conjugacao_expandido_v2(self.permutacoes, self.tabela_mult)

#     @staticmethod
#     def gerar_operacoes_conjugacao_expandido_v2(dicionario_perms, tabela_mult, destino_tex="analise/registro_classes_expandido.tex"):

#         nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
#         nomes = list(dicionario_perms.keys())
#         perms = list(dicionario_perms.values())
#         linhas = ["\\begin{align*}"]

#         id_idx = nomes.index("\\mathrm{E}")

#         for h_idx, h in enumerate(nomes):
#             for g_idx, g in enumerate(nomes):
#                 for k_idx, k_nome in enumerate(nomes):
#                     if tabela_mult[h_idx][k_idx] == "\\mathrm{E}":
#                         h_inv = nomes[k_idx]
#                         break
#                 else:
#                     h_inv = "?"

#                 ph = dicionario_perms[h]
#                 pg = dicionario_perms[g]
#                 ph_inv = dicionario_perms[h_inv] if h_inv in dicionario_perms else []

#                 hgh = [ph[i] for i in pg]
#                 conj = [hgh[i] for i in ph_inv] if ph_inv else []

#                 g_conj = nome_por_perm.get(tuple(conj), "?")

#                 linhas.append(
#                     f"& {h} {g} {h}^{{-1}} = {g_conj} \\quad "
#                     f"\\text{{perm: }}({', '.join(map(str, ph))})"
#                     f"({', '.join(map(str, pg))})"
#                     f"({', '.join(map(str, ph_inv))})"
#                     f" = ({', '.join(map(str, conj))}) \\\\"
#                 )

#         linhas.append("\\end{align*}")
#         Path(destino_tex).write_text("\n".join(linhas), encoding="utf-8")
#         return destino_tex

#     @staticmethod
#     def detectar_classes_conjugacao(dicionario_perms):
#         """Description
        
#         Args:
#             dicionario_perms (TYPE): Description
        
#         Returns:
#             TYPE: Description
#         """
#         nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
#         nomes = list(dicionario_perms.keys())
#         permutacoes = list(dicionario_perms.values())

#         classes = []
#         visitados = set()

#         for i, g in enumerate(permutacoes):
#             if i in visitados:
#                 continue
#             classe = set()
#             for h in permutacoes:
#                 h_inv = [h.index(j) for j in range(len(h))]
#                 conjugado = [h[g[i]] for i in h_inv]
#                 classe.add(tuple(conjugado))
#             indices_classe = [j for j, p in enumerate(permutacoes) if tuple(p) in classe]
#             visitados.update(indices_classe)
#             classes.append(indices_classe)

#         return classes




#     @classmethod
#     def salvar_classes_conjugacao(cls, classes, path_txt="analise/classes.txt", path_tex="analise/classes.tex"):
#         """Description
        
#         Args:
#             classes (TYPE): Description
#             path_txt (str, optional): Description
#             path_tex (str, optional): Description
#         """
#         unicas = list({frozenset(v) for v in classes.values()})
#         unicas.sort(key=lambda s: sorted(list(s))[0])

#         Path("analise").mkdir(exist_ok=True)

#         with open(path_txt, "w", encoding="utf-8") as f_txt:
#             for idx, classe in enumerate(unicas, 1):
#                 f_txt.write(f"Classe {idx}: " + ", ".join(sorted(classe)) + "\n")

#         with open(path_tex, "w", encoding="utf-8") as f_tex:
#             f_tex.write("\\begin{itemize}\n")
#             for idx, classe in enumerate(unicas, 1):
#                 itens = ", ".join(cls.nome_para_latex(n) for n in sorted(classe))
#                 f_tex.write(f"  \\item Classe {idx}: {itens}\n")
#             f_tex.write("\\end{itemize}\n")