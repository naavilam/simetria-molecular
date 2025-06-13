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
                \section{Operações de Multiplicação}
                \subsection{Tabela de Multiplicação}
                \begin{adjustbox}{max width=\linewidth, angle=90, center}
                \[
                %s
                \]
                \end{adjustbox}
                """ % self._formatar_tabela_multiplicacao(self.resultado['operacoes_multiplicacao']))

            blocos.append(r"""
                \subsection{Operações de Multiplicação Detalhadas}
                \begin{longtable}{>{$}r<{$} >{$}l<{$} >{$}l<{$}}
                %s
                \end{longtable}
                """ % self._formatar_operacoes_multiplicacao(self.resultado['operacoes_multiplicacao']))

        if "operacoes_conjugacao" in self.resultado:
            classes = self._extrair_classes_de_operacoes(self.resultado["operacoes_conjugacao"])

            blocos.append(r"""
                \section{Operações de Conjugação}
                \subsection{Tabela de Conjugação}
                \begin{adjustbox}{max width=\linewidth, angle=90, center}
                \begin{longtable}{l}
                %s
                \end{longtable}
                \end{adjustbox}
                """ % self._formatar_tabela_conjugacao(self.resultado["operacoes_conjugacao"]))

            blocos.append(r"""
                \subsection{Operações de Conjugação Detalhadas}
                %s
                """ % self._formatar_operacoes_conjugacao(self.resultado["operacoes_conjugacao"]))

            blocos.append(r"""
                \subsection{Agrupamento em Classes de Conjugação}
                \begin{itemize}
                %s
                \end{itemize}
                """ % "\n".join(
                    f"\\item \\textbf{{{classe}}}: {', '.join(f'${op}$' for op in ops)}"
                    for classe, ops in classes.items()
                ))

        return fr"""\documentclass[a4paper,12pt]{{article}}
        \usepackage{{datetime2}}
        \usepackage{{graphicx}}
        \usepackage[utf8]{{inputenc}}
        \usepackage{{fancyhdr}}
        \usepackage{{geometry}}
        \usepackage{{amsmath}}
        \usepackage{{longtable}}
        \usepackage{{lastpage}}
        \usepackage[hidelinks]{{hyperref}}
        \usepackage{{adjustbox}}
        \usepackage{{lscape}}  % ou rotfloat, caso queira controlar melhor

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

        linhas.append("\\begin{array}{c|" + "c" * len(chaves) + "}")
        linhas.append(" & " + " & ".join(f"{op}" for op in chaves) + r" \\ \hline")

        for op1, linha in tabela.items():
            valores = [linha[op2]["nome"] for op2 in chaves]
            linhas.append(f"{op1} & " + " & ".join(valores) + r" \\")

        linhas.append("\\end{array}")
        return "\n".join(linhas)

    def _formatar_operacoes_multiplicacao(self, operacoes: dict) -> str:
        linhas = []
        for op1, linha in operacoes.items():
            for op2, info in linha.items():
                perm2 = info["permutacao_op2"]
                perm_result = info["permutacao_resultante"]
                resultado = info["nome"]
                linhas.append(
                    rf"\makebox[3.3cm][r]{{$\mathrm{{{op1}}} \circ \mathrm{{{op2}}}$}} &="
                    rf" $\mathrm{{{op1}}} \circ {perm2}$ &="
                    rf" ${perm_result}$ &="
                    rf" \makebox[2.3cm][l]{{$\mathrm{{{resultado}}}$}} \\"
                )
        return "\n".join(linhas)

    def _formatar_operacoes_conjugacao(self, operacoes: dict) -> str:
        linhas = []
        for g, conjugacoes in operacoes.items():
            linhas.append(f"\\subsection*{{Conjugações de ${g}$}}")
            for h, info in conjugacoes.items():
                g_perm = info['detalhe']['g']
                h_perm = info['detalhe']['h']
                hgh_inv = info['detalhe']['hgh⁻¹']
                res = info['resultado']
                linhas.append(
                    rf"$\mathrm{{{h}}} \circ \mathrm{{{g}}} \circ \mathrm{{{h}}}^{{-1}} = {hgh_inv} = \mathrm{{{res}}}$ \\"
                )
        return "\n".join(linhas)

    @staticmethod
    def _extrair_classes_de_operacoes(operacoes: dict) -> dict:
        """
        Agrupa elementos conjugados em classes disjuntas.
        Cada par (g, resultado) da conjugação entra no mesmo conjunto.
        """
        nomes = sorted({g for g in operacoes} |
                       {h for conj in operacoes.values() for h in conj} |
                       {info["resultado"] for conj in operacoes.values() for info in conj.values()})

        grupos = []

        def encontrar_grupo(elem):
            for grupo in grupos:
                if elem in grupo:
                    return grupo
            return None

        for g, conjugacoes in operacoes.items():
            for h, info in conjugacoes.items():
                res = info["resultado"]

                grupo_g = encontrar_grupo(g)
                grupo_res = encontrar_grupo(res)

                if grupo_g and grupo_res:
                    if grupo_g is not grupo_res:
                        grupo_g.update(grupo_res)
                        grupos.remove(grupo_res)
                elif grupo_g:
                    grupo_g.add(res)
                elif grupo_res:
                    grupo_res.add(g)
                else:
                    grupos.append(set([g, res]))

        return {
            f"Classe {i+1}": sorted(grupo, key=nomes.index)
            for i, grupo in enumerate(grupos)
        }


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

    @staticmethod
    def latex_safe(op: str) -> str:
        """
        Corrige superscript/subscript duplos como \mathrm{C}_{2}^{(a)} para evitar erro de compilação LaTeX.
        """
        return re.sub(r"(\\mathrm\{[A-Za-z]+\})_\{([^\}]+)\}\^\{([^\}]+)\}",
                      r"\1_{\2}^{\3}", op)