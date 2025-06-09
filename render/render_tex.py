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
        blocos = []

        if "permutacoes" in self.resultado:
            blocos.append(r"""
                \section*{Permutações Básicas}
                \[
                %s
                \]
                """ % self._formatar_permutacoes(self.resultado['permutacoes']))

        if "tabela" in self.resultado:
            blocos.append(r"""
                \section*{Tabela de Multiplicação}
                \[
                %s
                \]
                """ % self._formatar_tabela_multiplicacao(self.resultado['tabela']))

            blocos.append(r"""
                \section*{Multiplicação de Operações}
                \begin{longtable}{ll}
                \textbf{Op1 * Op2} & \textbf{Resultado} \\
                %s
                \end{longtable}
                """ % self._formatar_operacoes_multiplicacao(self.resultado['tabela']))

        if "classes" in self.resultado:
            blocos.append(r"""
                \section*{Classes de Conjugação}
                \[
                %s
                \]
                """ % self._formatar_classes(self.resultado['classes']))

            blocos.append(r"""
                \section*{Operações por Classe}
                %s
                """ % self._formatar_operacoes_por_classe(self.resultado['classes']))

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
        \vspace*{{2em}}
        {''.join(blocos)}
        \end{{document}}
        """

    def _formatar_permutacoes(self, permutacoes: dict) -> str:
        linhas = ["\\begin{array}{r@{\\,:\\ }l}"]
        for nome, lista in permutacoes.items():
            linhas.append(f"\\mathrm{{{nome}}} & {lista} \\\\")
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