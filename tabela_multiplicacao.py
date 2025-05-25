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
from pathlib import Path

class TabelaMultiplicacao:

    def __init__(self, permutacoes):
        """Summary
        """
        self.permutacoes = permutacoes

    def gerar(self, registro_txt="registro_operacoes.txt", registro_tex="registro_operacoes.tex"):
        """Calcula tabela de multiplicação
        
        Args:
            dicionario_perms (TYPE): Description
            registro_txt (str, optional): Description
            registro_tex (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        nomes = list(self.permutacoes.keys())
        perms = list(self.permutacoes.values())
        hash_perms = self._gerar_hash_permutacoes()

        tabela = []
        log_txt = []
        log_tex = ["\\begin{align*}"]

        for i, pi in enumerate(perms):
            linha = []
            for j, pj in enumerate(perms):
                nome_i = nomes[i]
                nome_j = nomes[j]
                comp = self._compor(pi, pj)
                nome_res = hash_perms.get(tuple(comp))

                if nome_res is None:
                    log_txt.append(f"⚠️ ERRO: {nome_i} * {nome_j} = ? (Permutação não encontrada)")
                    continue

                linha.append(nome_res)
                log_txt.append(f"{nome_i} * {nome_j} = {nome_res}")
                log_txt.append(f"  {pi} ∘ {pj} = {comp}")

                def perm_str(v):
                    """Description
                    
                    Args:
                        v (TYPE): Description
                    
                    Returns:
                        TYPE: Description
                    """
                    return "(" + ",".join(str(x + 1) for x in v) + ")"

                li, lj, lr = map(lambda n: self._nome_para_latex(n).replace('\\\\', '\\'), [nome_i, nome_j, nome_res])
                log_tex.append(
                    f"& {lr} = {lj} \\circ {li}:\\; \\\\"
                    f"& {perm_str(list(range(len(pi))))} \\xrightarrow{{{li}}} {perm_str(pi)} "
                    f"\\xrightarrow{{{lj}}} {perm_str(comp)}, \\\\"
                )
            tabela.append(linha)

        log_tex.append("\\end{align*}")

        # Arquivos
        output_dir = Path("analise")
        output_dir.mkdir(exist_ok=True)

        Path(output_dir / "registro_operacoes_multiplicacao.txt").write_text("\n".join(log_txt), encoding="utf-8")
        Path(output_dir / "registro_operacoes_multiplicacao.tex").write_text("\n".join(log_tex), encoding="utf-8")

        with open(output_dir / "tabela_multiplicacao.txt", "w") as f_txt:
            for nome, linha in zip(nomes, tabela):
                f_txt.write(f"{nome}: " + " ".join(linha) + "\n")

        with open(output_dir / "tabela_multiplicacao.tex", "w") as f_tex:
            f_tex.write(self._gerar_tabela_latex(nomes, tabela))

        print("Tabelas e registros de multiplicação gerados com sucesso.")
        return tabela
    def _compor(self, p1, p2):
        """Description
        
        Args:
            p1 (TYPE): Description
            p2 (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return [p1[i] for i in p2]

    def _gerar_hash_permutacoes(self):
        """Description
        
        Args:
            dicionario_perms (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return {tuple(p): nome for nome, p in self.permutacoes.items()}

    def _nome_para_latex(self, nome, wrap_math=False):
        """Description
        
        Args:
            nome (TYPE): Description
            wrap_math (bool, optional): Description
        
        Returns:
            TYPE: Description
        """
        nome = nome.replace("'", "^{\\prime}").replace("²", "^2")
        nome = nome.replace("sigma_v", "sigma_{v}")
        nome = nome.replace("sigma_d", "sigma_{d}")
        nome = nome.replace("sigma_h", "sigma_{h}")
        nome = re.sub(r"(C[2346])_\((\w)\)", r"\\mathrm{\1}^{(\2)}", nome)
        nome = re.sub(r"(C[2346])", r"\\mathrm{\1}", nome)
        nome = re.sub(r"(S[36])", r"\\mathrm{\1}", nome)
        nome = re.sub(r"\bsigma_?(v\d+)", r"\\sigma_{\1}", nome)
        nome = re.sub(r"\bsigma", r"\\sigma", nome)
        return f"${nome}$" if wrap_math else nome

    def _gerar_tabela_latex(self, nomes, tabela):
        """Description
        
        Args:
            nomes (TYPE): Description
            tabela (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        colunas = "c|" + "c" * len(nomes)
        linhas = ["\\begin{tabular}{" + colunas + "}", "\\toprule"]
        linhas.append(" & " + " & ".join(f"${n}$" for n in nomes) + " \\\\")
        linhas.append("\\midrule")
        for nome, linha in zip(nomes, tabela):
            linhas.append(f"${nome}$ & " + " & ".join(f"${x}$" for x in linha) + " \\\\")
        linhas.append("\\bottomrule\n\\end{tabular}")
        return "\n".join(linhas)

    def _imprimir_tabela_texto(self, nomes, tabela):
        """Description
        
        Args:
            nomes (TYPE): Description
            tabela (TYPE): Description
        """
        print("     " + " ".join(f"{n:>6}" for n in nomes))
        for nome, linha in zip(nomes, tabela):
            print(f"{nome:>5} " + " ".join(f"{val:>6}" for val in linha))