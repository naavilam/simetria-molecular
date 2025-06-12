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
import re

class LatexReportGenerator:
    def __init__(self, metadata, resultado):
        self.metadata = metadata
        self.resultado = resultado

    def gerar_documento(self):
        blocos = []

        if "permutacoes" in self.resultado:
            blocos.append(r"""
                \section{Permutações Básicas}
                \[
                %s
                \]
                """ % self._formatar_permutacoes(self.resultado['permutacoes']))

        if "operacoes_multiplicacao" in self.resultado:
            blocos.append(r"""
                \section{Tabela de Multiplicação}
                \[
                %s
                \]
                """ % self._formatar_tabela_multiplicacao(self.resultado['operacoes_multiplicacao']))

            blocos.append(r"""
                \section{Multiplicação de Operações}
                \begin{longtable}{ll}
                \textbf{Op1 * Op2} & \textbf{Resultado} \\
                %s
                \end{longtable}
                """ % self._formatar_operacoes_multiplicacao(self.resultado['operacoes_multiplicacao']))

        if "operacoes_conjugacao" in self.resultado:
            classes = self._extrair_classes_de_operacoes(self.resultado["operacoes_conjugacao"])

            blocos.append(r"""
                \section{Classes de Conjugação}
                \[
                %s
                \]
                """ % self._formatar_tabela_conjugacao(self.resultado["operacoes_conjugacao"]))

            blocos.append(r"""
                \section{Operações por Classe}
                %s
                """ % self._formatar_operacoes_conjugacao(self.resultado["operacoes_conjugacao"]))

            blocos.append(r"""
                \section{Agrupamento Final em Classes}
                \begin{itemize}
                %s
                \end{itemize}
                """ % "\n".join(
                    f"\\item \\textbf{{{classe}}}: {', '.join(ops)}"
                    for classe, ops in classes.items()
                ))

          # if "operacoes_conjugacao" in self.resultado:
        #     blocos.append(r"""
        #         \section{Classes de Conjugação}
        #         \[
        #         %s
        #         \]
        #         """ % self._formatar_tabela_conjugacao(self.resultado['operacoes_conjugacao']))

        #     blocos.append(r"""
        #         \section{Operações por Classe}
        #         %s
        #         """ % self._formatar_operacoes_conjugacao(self.resultado['operacoes_conjugacao']))

        return fr"""\documentclass[a4paper,12pt]{{article}}
        \usepackage{{datetime2}}
        \usepackage{{graphicx}}
        \usepackage[utf8]{{inputenc}}
        \usepackage{{fancyhdr}}
        \usepackage{{geometry}}
        \usepackage{{amsmath}}
        \usepackage{{longtable}}
        \usepackage{{lastpage}}

        \geometry{{left=1cm, right=1cm, top=2.5cm, bottom=2.5cm}}
        \pagestyle{{fancy}}
        \fancyhf{{}}

        \setlength{{\headheight}}{{35pt}}  % altura reservada para o cabeçalho
        \setlength{{\headsep}}{{2em}}      % espaço entre cabeçalho e corpo

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

        \fancyfoot[L]{{\scriptsize {{\tiny \textcopyright}} naavilam.github.io/simetria-molecular contact@chanah.dev}}

        \begin{{document}}

        \tableofcontents
        \newpage

        {''.join(blocos)}
        \end{{document}}
        """

    def _formatar_permutacoes(self, permutacoes: dict) -> str:
        linhas = ["\\begin{array}{r@{\\,:\\ }l}"]
        for nome, lista in permutacoes.items():
            linhas.append(f"\\mathrm{{{nome}}} & {lista} \\\\")
        linhas.append("\\end{array}")
        return "\n".join(linhas)

    def _formatar_tabela_multiplicacao(self, tabela: dict) -> str:
        chaves = list(tabela.keys())
        linhas = []

        # Cabeçalho do array
        linhas.append("\\begin{array}{c|" + "c" * len(chaves) + "}")
        linhas.append(" & " + " & ".join(f"{op}" for op in chaves) + r" \\ \hline")

        # Corpo da tabela
        for op1, linha in tabela.items():
            valores = [linha[op2] for op2 in chaves]
            linhas.append(f"{op1} & " + " & ".join(valores) + r" \\")

        linhas.append("\\end{array}")
        return "\n".join(linhas)

    def _formatar_operacoes_multiplicacao(self, tabela: dict) -> str:
        linhas = []
        for op1, linha in tabela.items():
            for op2, resultado in linha.items():
                linhas.append(f"${op1} * {op2}$ & ${resultado}$ \\\\")
        return "\n".join(linhas)

    # def _formatar_classes(self, classes) -> str:
    #     linhas = ["\\begin{array}{r@{\\,:\\ }l}"]
    #     for nome, classe in classes.items():
    #         linhas.append(f"{nome} & {classe} \\")
    #     linhas.append("\\end{array}")
    #     return "\n".join(linhas)

    def _formatar_operacoes_conjugacao(self, operacoes: dict) -> str:
        linhas = []

        for g, conjugacoes in operacoes.items():
            linhas.append(f"\\subsection{{Conjugações de ${g}$}}")
            for h, info in conjugacoes.items():
                res = info['resultado']
                g_perm = info['detalhe']['g']
                h_perm = info['detalhe']['h']
                hgh_inv = info['detalhe']['hgh⁻¹']

                linhas.append(
                    f"$ {h} \\circ {g} \\circ ({h})^{{-1}} = {hgh_inv} = {res}$ \\\\[1em]"
                )

        return "\n".join(linhas)

    # @staticmethod
    # def _extrair_classes_de_operacoes(operacoes_conjugacao: dict) -> dict:
    #     nomes = list(operacoes_conjugacao.keys())
    #     visitados = set()
    #     classes = []

    #     for g in nomes:
    #         if g in visitados:
    #             continue

    #         classe = set()
    #         # inclui o próprio g
    #         classe.add(g)

    #         # percorre todos os h conjugando g
    #         for h in operacoes_conjugacao[g]:
    #             nome_k = operacoes_conjugacao[g][h]['resultado']
    #             classe.add(nome_k)

    #         # evita repetição
    #         if not any(classe & c for c in classes):
    #             classes.append(classe)
    #             visitados.update(classe)

    #     # Formatar como {"Classe 1": [...], ...}
    #     return {f"Classe {i+1}": sorted(list(c), key=nomes.index) for i, c in enumerate(classes)}

    def _extrair_classes_de_operacoes(self, operacoes: dict) -> dict:
        # Coletar todos os nomes envolvidos para ordenação
        nomes = sorted({g for g in operacoes} |
                       {h for conj in operacoes.values() for h in conj} |
                       {info['resultado'] for conj in operacoes.values() for info in conj.values()})

        # Agrupar por classes (evitar repetições usando set congelado)
        conjuntos = {}
        for g, conjugacoes in operacoes.items():
            classe = frozenset([info['resultado'] for info in conjugacoes.values()])
            conjuntos.setdefault(classe, set()).add(g)

        # Renomear como Classe 1, Classe 2, etc
        return {f"Classe {i+1}": sorted(list(c), key=nomes.index) for i, c in enumerate(conjuntos)}

    def _formatar_tabela_conjugacao(self, operacoes: dict) -> str:
        nomes = list(operacoes.keys())
        linhas = []

        linhas.append("\\begin{array}{c|" + "c" * len(nomes) + "}")
        linhas.append(" & " + " & ".join(nomes) + " \\\\ \\hline")

        for g, resultados in operacoes.items():
            linha = [g]
            for h in nomes:
                linha.append(resultados[h]['resultado'])
            linhas.append(" & ".join(linha) + " \\\\")
        linhas.append("\\end{array}")
        return "\n".join(linhas)

    # def _formatar_operacoes_por_classe(self, classes) -> str:
    #     agrupadas = {}
    #     for op, classe in classes.items():
    #         agrupadas.setdefault(str(classe), []).append(op)

    #     blocos = []
    #     for idx, (classe, ops) in enumerate(agrupadas.items(), start=1):
    #         blocos.append(f"\\subsection*{{Classe {idx}}}\n\\begin{{itemize}}")
    #         for op in ops:
    #             blocos.append(f"  \item ${op}$")
    #         blocos.append("\\end{itemize}")
    #     return "\n".join(blocos)

    @staticmethod
    def latex_safe(op: str) -> str:
        """
        Corrige superscript/subscript duplos como \mathrm{C}_{2}^{(a)} para evitar erro de compilação LaTeX.
        """
        return re.sub(r"(\\mathrm\{[A-Za-z]+\})_\{([^\}]+)\}\^\{([^\}]+)\}",
                      r"\1_{\2}^{\3}", op)