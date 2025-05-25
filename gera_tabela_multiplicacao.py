
import json
import re
import unicodedata
from pathlib import Path

# Def: compor
def compor(p1, p2):
    return [p1[i] for i in p2]

# Def: gerar_hash_permutacoes
def gerar_hash_permutacoes(dicionario_perms):
    return {tuple(p): nome for nome, p in dicionario_perms.items()}

# Def: nome_para_latex
def nome_para_latex(nome, wrap_math=False):
    nome = nome.replace("'", "^{\\prime}")
    nome = nome.replace("²", "^2")

    # primeiro: substituições literais
    nome = nome.replace("sigma_v", "sigma_{v}")
    nome = nome.replace("sigma_d", "sigma_{d}")
    nome = nome.replace("sigma_h", "sigma_{h}")

    # agora as regex
    nome = re.sub(r"(C[2346])_\((\w)\)", r"\\mathrm{\1}^{(\2)}", nome)
    nome = re.sub(r"(C[2346])", r"\\mathrm{\1}", nome)
    nome = re.sub(r"(S[36])", r"\\mathrm{\1}", nome)
    nome = re.sub(r"\bsigma_?(v\d+)", r"\\sigma_{\1}", nome)
    nome = re.sub(r"\bsigma", r"\\sigma", nome)

    return f"${nome}$" if wrap_math else nome

# Def: gerar_tabela_multiplicacao
def gerar_tabela_multiplicacao(dicionario_perms, registro_txt="registro_operacoes.txt", registro_tex="registro_operacoes.tex"):
    nomes = list(dicionario_perms.keys())
    permutacoes = list(dicionario_perms.values())
    hash_perms = gerar_hash_permutacoes(dicionario_perms)

    tabela = []
    registro_txt_linhas = []
    registro_tex_linhas = ["\\begin{align*}"]

    for i in range(len(permutacoes)):
        linha = []
        for j in range(len(permutacoes)):
            nome_i = nomes[i]
            nome_j = nomes[j]
            pi = permutacoes[i]
            pj = permutacoes[j]
            comp = compor(pi, pj)
            nome_resultado = hash_perms.get(tuple(comp))

            if nome_resultado is None:
                registro_txt_linhas.append(f"⚠️ ERRO: {nome_i} * {nome_j} = ? (Permutação não encontrada)")
                continue

            linha.append(nome_resultado)

            # TXT
            registro_txt_linhas.append(f"{nome_i} * {nome_j} = {nome_resultado}")
            registro_txt_linhas.append(f"  {pi} ∘ {pj} = {comp}")

            # LaTeX
            latex_i = nome_para_latex(nome_i, wrap_math=False).replace('\\\\', '\\')
            latex_j = nome_para_latex(nome_j, wrap_math=False).replace('\\\\', '\\')
            latex_r = nome_para_latex(nome_resultado, wrap_math=False).replace('\\\\', '\\')
            
            # Def: perm_str
            def perm_str(v): return "(" + ",".join(str(x + 1) for x in v) + ")"
            registro_tex_linhas.append(
                f"& {latex_r} = {latex_j} \\circ {latex_i}:\\; \\\\"
                f"& {perm_str(list(range(len(pi))))} \\xrightarrow{{{latex_i}}} {perm_str(pi)} "
                f"\\xrightarrow{{{latex_j}}} {perm_str(comp)}, \\\\"
            )

        tabela.append(linha)

    registro_tex_linhas.append("\\end{align*}")

    output_dir = Path("analise")
    output_dir.mkdir(exist_ok=True)

    path_txt = output_dir / "tabela_multiplicacao.txt"
    path_tex = output_dir / "tabela_multiplicacao.tex"

    path_txt_rg = output_dir / "registro_operacoes_multiplicacao.txt"
    path_tex_rg = output_dir / "registro_operacoes_multiplicacao.tex"

    Path(path_txt_rg).write_text("\n".join(registro_txt_linhas), encoding="utf-8")
    Path(path_tex_rg).write_text("\n".join(registro_tex_linhas), encoding="utf-8")

    with open(path_txt, "w") as f:
        for nome, linha in zip(nomes, tabela):
            f.write(f"{nome}: " + " ".join(linha) + "\n")

    with open(path_tex, "w") as f:
        f.write(gerar_tabela_latex(nomes, tabela))

    print("Tabelas de multiplicação geradas: tabela_multiplicacao.txt e tabela_multiplicacao.tex")
    print("Registros de operações de multiplicação gerados: registro_operacoes_multiplicacao.txt e registro_operacoes_multiplicacoes.tex")
    return tabela

# Def: imprimir_tabela_texto
def imprimir_tabela_texto(nomes, tabela):
    header = "     " + " ".join(f"{nome:>6}" for nome in nomes)
    print(header)
    for nome, linha in zip(nomes, tabela):
        print(f"{nome:>5} " + " ".join(f"{val:>6}" for val in linha))

# Def: gerar_tabela_latex
def gerar_tabela_latex(nomes, tabela):
    colunas = "|c|" + "c|" * len(nomes)
    linhas = [f"\begin{{tabular}}{{{colunas}}}\hline"]
    linhas.append(" & " + " & ".join(nomes) + " \\ \hline")
    for nome, linha in zip(nomes, tabela):
        linhas.append(f"{nome} & " + " & ".join(linha) + " \\ \hline")
    linhas.append("\end{tabular}")
    return "\n".join(linhas)

# Def: gerar_tabela_latex
def gerar_tabela_latex(nomes, tabela):
    colunas = "c|" + "c" * len(nomes)
    linhas = ["\\begin{tabular}{" + colunas + "}", "\\toprule"]

    # Cabeçalho
    header = " & " + " & ".join(f"${n}$" for n in nomes) + " \\\\"
    linhas.append(header)
    linhas.append("\\midrule")

    # Corpo da tabela
    for nome_linha, linha in zip(nomes, tabela):
        row = f"${nome_linha}$ & " + " & ".join(f"${x}$" for x in linha) + " \\\\"
        linhas.append(row)

    linhas.append("\\bottomrule")
    linhas.append("\\end{tabular}")
    return "\n".join(linhas)

