import json
import re
import unicodedata
from operacoes_latex_dict import operacoes_latex

def gerar_tabela_multiplicacao(dicionario_perms, registro_path="registro_operacoes.txt"):
    nomes = list(dicionario_perms.keys())
    permutacoes = list(dicionario_perms.values())
    hash_perms = gerar_hash_permutacoes(dicionario_perms)

    tabela = []
    registro = []

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
                registro.append(f"⚠️ ERRO: {nome_i} * {nome_j} = ? (Permutação não encontrada)")
            else:
                registro.append(f"{nome_i} * {nome_j} = {nome_resultado}")
                registro.append(f"  {pi} ∘ {pj} = {comp}")

            linha.append(nome_resultado)
        tabela.append(linha)

    # Salvar registro detalhado (se desejado)
    if registro_path:
        with open(registro_path, "w", encoding="utf-8") as f:
            f.write("\n".join(registro))

    return nomes, tabela

def compor(p1, p2):
    return [p1[i] for i in p2]

def gerar_hash_permutacoes(dicionario_perms):
    return {tuple(p): nome for nome, p in dicionario_perms.items()}

def imprimir_tabela_texto(nomes, tabela):
    header = "     " + " ".join(f"{nome:>6}" for nome in nomes)
    print(header)
    for nome, linha in zip(nomes, tabela):
        print(f"{nome:>5} " + " ".join(f"{val:>6}" for val in linha))

def gerar_tabela_latex(nomes, tabela):
    colunas = "|c|" + "c|" * len(nomes)
    linhas = [f"\begin{{tabular}}{{{colunas}}}\hline"]
    linhas.append(" & " + " & ".join(nomes) + " \\ \hline")
    for nome, linha in zip(nomes, tabela):
        linhas.append(f"{nome} & " + " & ".join(linha) + " \\ \hline")
    linhas.append("\end{tabular}")
    return "\n".join(linhas)

def nome_para_latex(nome):
    nome = nome.replace("'", "^{\\prime}")
    nome = nome.replace("²", "^2")
    nome = re.sub(r"(C[2346])_\((\w)\)", r"\\mathrm{\1}^{(\2)}", nome)
    nome = re.sub(r"(C[2346])", r"\\mathrm{\1}", nome)
    nome = re.sub(r"(S[36])", r"\\mathrm{\1}", nome)
    nome = re.sub(r"(\bsigma)_?(v\d+)", r"\\sigma_{\2}", nome)
    nome = re.sub(r"(\bsigma)", r"\\sigma", nome)
    nome = re.sub(r"(\\sigma)_?(v\d+)", r"\\sigma_{\2}", nome)
    nome = nome.replace("sigma_v", "sigma_{v}")
    nome = nome.replace("sigma_d", "sigma_{d}")
    nome = nome.replace("sigma_h", "sigma_{h}")
    return f"${nome}$"

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

