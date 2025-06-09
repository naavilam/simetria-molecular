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

# latex_generator.py
from datetime import datetime

class LatexReportGenerator:
    def __init__(self, metadata, resultado):
        self.metadata = metadata
        self.resultado = resultado

    def gerar_documento(self):
        return fr"""\documentclass[a4paper,12pt]{{article}}
        \usepackage{{datetime2}}
        \usepackage{{graphicx}}
        \usepackage[utf8]{{inputenc}}
        \usepackage{{fancyhdr}}
        \usepackage{{geometry}}
        \usepackage{{amsmath}}
        \usepackage{{longtable}}
        \geometry{{left=1cm, right=1cm, top=2.5cm, bottom=2cm}}
        \pagestyle{{fancy}}
        \fancyhf{{}}

        % Cabeçalho
        \fancyhead[L]{{\textbf{{Análise de Simetria}} \\
        \textbf{{Sistema {self.metadata['sistema']}}} \\
        Tempo de Execução: \textbf{{{self.resultado['tempo_execucao']}}}}}

        \fancyhead[C]{{Molécula: \textbf{{{self.metadata['molecula']}}} \\
        Grupo: \textbf{{{self.metadata['grupo']}}} \\
        Ordem: \textbf{{{self.metadata['ordem']}}}}}

        \fancyhead[R]{{{self.metadata['data']} \\
        Relatório: \textbf{{{self.metadata['uuid']}}} \\
        Página \thepage\ de \pageref{{LastPage}}}}

        \fancyfoot[L]{{\scriptsize {{\tiny \textcopyright}} naavilam.github.io/simetria-molecular 
        \includegraphics[height=1.1ex]{{image2.jpg}} contact@chanah.dev}}

        \begin{{document}}
        \section*{{Permutações Básicas}}
        \[
        {self._formatar_permutacoes(self.resultado['permutacoes'])}
        \]
        \section*{{Tabela de Multiplicação}}
        \[
        {self._formatar_tabela_multiplicacao(self.resultado['tabela'])}
        \]
        \section*{{Multiplicação de Operações}}
        \begin{{longtable}}{{ll}}
        \textbf{{Op1 * Op2}} & \textbf{{Resultado}} \\
        {self._formatar_operacoes_multiplicacao(self.resultado['tabela'])}
        \end{{longtable}}
        \section*{{Classes de Conjugação}}
        \[
        {self._formatar_classes(self.resultado['classes'])}
        \]
        \section*{{Operações por Classe}}
        {self._formatar_operacoes_por_classe(self.resultado['classes'])}
        \end{{document}}
        """

    def _formatar_permutacoes(self, permutacoes: dict) -> str:
        linhas = ["\\begin{array}{r@{\\,:\\ }l}"]
        for nome, lista in permutacoes.items():
            linhas.append(f"{nome} & {lista} \\")
        linhas.append("\\end{array}")
        return "\n".join(linhas)

    def _formatar_tabela_multiplicacao(self, tabela) -> str:
        return tabela

    def _formatar_operacoes_multiplicacao(self, tabela) -> str:
        linhas = []
        for op1, linha in tabela.items():
            for op2, resultado in linha.items():
                linhas.append(f"${op1} * {op2}$ & ${resultado}$ \\")
        return "\n".join(linhas)

    def _formatar_classes(self, classes) -> str:
        linhas = ["\\begin{array}{r@{\\,:\\ }l}"]
        for nome, classe in classes.items():
            linhas.append(f"{nome} & {classe} \\")
        linhas.append("\\end{array}")
        return "\n".join(linhas)

    def _formatar_operacoes_por_classe(self, classes) -> str:
        agrupadas = {}
        for op, classe in classes.items():
            agrupadas.setdefault(str(classe), []).append(op)

        blocos = []
        for idx, (classe, ops) in enumerate(agrupadas.items(), start=1):
            blocos.append(f"\\subsection*{{Classe {idx}}}\n\\begin{{itemize}}")
            for op in ops:
                blocos.append(f"  \item ${op}$")
            blocos.append("\\end{itemize}")
        return "\n".join(blocos)


# def _formatar_latex(self, tabela):
#         colunas = len(tabela[0])
#         latex = ["\\begin{array}{" + "c" * colunas + "}"]
#         for linha in tabela:
#             latex.append(" & ".join(linha) + " \\")
#         latex.append("\\end{array}")
#         return "\n".join(latex)

        # def _gerar_tabela_latex(self, nomes, tabela):
        # """Description
        
        # Args:
        #     nomes (TYPE): Description
        #     tabela (TYPE): Description
        
        # Returns:
        #     TYPE: Description
        # """
        # colunas = "c|" + "c" * len(nomes)
        # linhas = ["\\begin{tabular}{" + colunas + "}", "\\toprule"]
        # linhas.append(" & " + " & ".join(f"${n}$" for n in nomes) + " \\\\")
        # linhas.append("\\midrule")
        # for nome, linha in zip(nomes, tabela):
        #     linhas.append(f"${nome}$ & " + " & ".join(f"${x}$" for x in linha) + " \\\\")
        # linhas.append("\\bottomrule\n\\end{tabular}")
        # return "\n".join(linhas)


    #         @staticmethod
    # def nome_para_latex(nome):
    #     """Description
        
    #     Args:
    #         nome (TYPE): Description
        
    #     Returns:
    #         TYPE: Description
    #     """
    #     nome = nome.replace("'", "^{\\prime}")
    #     nome = nome.replace("²", "^2")
    #     nome = nome.replace("sigma_v", "sigma_{v}")
    #     nome = nome.replace("sigma_d", "sigma_{d}")
    #     nome = nome.replace("sigma_h", "sigma_{h}")
    #     nome = re.sub(r"(C[2346])_\((\w)\)", r"\\mathrm{\1}^{(\2)}", nome)
    #     nome = re.sub(r"(C[2346])", r"\\mathrm{\1}", nome)
    #     nome = re.sub(r"(S[36])", r"\\mathrm{\1}", nome)
    #     nome = re.sub(r"\bsigma_?(v\d+)", r"\\sigma_{\1}", nome)
    #     nome = re.sub(r"\bsigma", r"\\sigma", nome)
    #     return f"${nome}$"



    #     @classmethod
    # def gerar_operacoes_conjugacao_latex(cls, dicionario_perms,
    #                                      destino_txt="analise/registro_classes.txt",
    #                                      destino_tex="analise/registro_classes.tex"):
        """Description
        
        Args:
            dicionario_perms (TYPE): Description
            destino_txt (str, optional): Description
            destino_tex (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        # nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
        # nomes = list(dicionario_perms.keys())
        # perms = list(dicionario_perms.values())
        # classes_idx = cls.detectar_classes_conjugacao(dicionario_perms)

        # tex = ["\\begin{align*}"]
        # txt = []

        # for idx, classe in enumerate(classes_idx, 1):
        #     tex.append(f"% Classe {idx}")
        #     txt.append(f"Classe {idx}:")
        #     for g_idx in classe:
        #         g = nomes[g_idx]
        #         pg = perms[g_idx]
        #         for h_idx in range(len(perms)):
        #             h = nomes[h_idx]
        #             ph = perms[h_idx]
        #             ph_inv = [ph.index(i) for i in range(len(ph))]
        #             conjugado = [ph[pg[i]] for i in ph_inv]
        #             g_conj = nome_por_perm.get(tuple(conjugado), "?")
        #             txt.append(f"{h} * {g} * {h}⁻¹ = {g_conj}")
        #             tex.append(f"& {h} {g} \\left({h}\\right)^{{-1}} = {g_conj} \\\\")

        # tex.append("")
        # tex.append("\\end{align*}")
        # Path(destino_txt).write_text("\n".join(txt), encoding="utf-8")
        # Path(destino_tex).write_text("\n".join(tex), encoding="utf-8")
        # return destino_txt, destino_tex

