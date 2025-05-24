import json
import re
from pathlib import Path

def compor(p1, p2):
    return [p1[i] for i in p2]

def gerar_classe_conjugacao(dicionario_perms, tab_mult):
    nomes = list(dicionario_perms.keys())
    perms = list(dicionario_perms.values())
    nome_por_perm = {tuple(p): nome for nome, p in dicionario_perms.items()}

    classes = {}
    for i, nome_i in enumerate(nomes):
        pi = perms[i]
        conj_class = set()
        for j, nome_j in enumerate(nomes):
            pj = perms[j]
            pj_inv = [pj.index(k) for k in range(len(pj))]
            comp1 = compor(pj, pi)
            conj = compor(comp1, pj_inv)
            nome_conjugado = nome_por_perm.get(tuple(conj))
            if nome_conjugado:
                conj_class.add(nome_conjugado)
        classes[nome_i] = conj_class
    salvar_classes_conjugacao(classes)
    gerar_operacoes_conjugacao_expandido_v2(dicionario_perms, tab_mult)
    return

def gerar_operacoes_conjugacao_expandido_v2(dicionario_perms, tabela_mult, destino_tex="analise/registro_classes_expandido.tex"):
    """
    Gera um arquivo LaTeX com detalhes da operação hgh⁻¹, consultando a tabela de multiplicação para h⁻¹.
    """
    nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
    nomes = list(dicionario_perms.keys())
    perms = list(dicionario_perms.values())
    linhas = ["\\begin{align*}"]

    id_idx = nomes.index("\\mathrm{E}")

    for h_idx, h in enumerate(nomes):
        for g_idx, g in enumerate(nomes):
            # Buscar índice de h⁻¹ tal que h * h⁻¹ = E
            for k_idx, k_nome in enumerate(nomes):
                if tabela_mult[h_idx][k_idx] == "\\mathrm{E}":
                    h_inv = nomes[k_idx]
                    break
            else:
                h_inv = "?"

            ph = dicionario_perms[h]
            pg = dicionario_perms[g]
            ph_inv = dicionario_perms[h_inv] if h_inv in dicionario_perms else []

            # hgh⁻¹
            hgh = [ph[i] for i in pg]
            conj = [hgh[i] for i in ph_inv] if ph_inv else []

            g_conj = nome_por_perm.get(tuple(conj), "?")

            # Linha LaTeX com detalhes
            linhas.append(
                f"& {h} {g} {h}^{{-1}} = {g_conj} \\quad "
                f"\\text{{perm: }}({', '.join(map(str, ph))})"
                f"({', '.join(map(str, pg))})"
                f"({', '.join(map(str, ph_inv))})"
                f" = ({', '.join(map(str, conj))}) \\\\"
            )

    linhas.append("\\end{align*}")
    Path(destino_tex).write_text("\n".join(linhas), encoding="utf-8")
    return destino_tex
def detectar_classes_conjugacao(dicionario_perms):
    nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
    nomes = list(dicionario_perms.keys())
    permutacoes = list(dicionario_perms.values())

    classes = []
    visitados = set()

    for i, g in enumerate(permutacoes):
        if i in visitados:
            continue
        classe = set()
        for h in permutacoes:
            h_inv = [h.index(j) for j in range(len(h))]
            conjugado = [h[g[i]] for i in h_inv]
            classe.add(tuple(conjugado))
        indices_classe = [j for j, p in enumerate(permutacoes) if tuple(p) in classe]
        visitados.update(indices_classe)
        classes.append(indices_classe)

    return classes

def gerar_operacoes_conjugacao_latex(dicionario_perms,
                                     destino_txt="analise/registro_classes.txt",
                                     destino_tex="analise/registro_classes.tex"):
    nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
    nomes = list(dicionario_perms.keys())
    perms = list(dicionario_perms.values())
    classes_idx = detectar_classes_conjugacao(dicionario_perms)

    tex = ["\\begin{align*}"]
    txt = []
    
    for idx, classe in enumerate(classes_idx, 1):
        tex.append(f"% Classe {idx}")
        txt.append(f"Classe {idx}:")
        for g_idx in classe:
            g = nomes[g_idx]
            pg = perms[g_idx]
            for h_idx in range(len(perms)):
                h = nomes[h_idx]
                ph = perms[h_idx]
                ph_inv = [ph.index(i) for i in range(len(ph))]
                conjugado = [ph[pg[i]] for i in ph_inv]
                g_conj = nome_por_perm.get(tuple(conjugado), "?")

                # Versão texto
                txt.append(f"{h} * {g} * {h}⁻¹ = {g_conj}")

                # Versão LaTeX com inverso corretamente formatado
                tex.append(f"& {h} {g} \\left({h}\\right)^{{-1}} = {g_conj} \\\\")

    tex.append("")

    tex.append("\\end{align*}")
    Path(destino_txt).write_text("\n".join(txt), encoding="utf-8")
    Path(destino_tex).write_text("\n".join(tex), encoding="utf-8")
    return destino_txt, destino_tex

# def gerar_operacoes_conjugacao_latex(dicionario_perms, destino_txt="analise/registro_classes.txt", destino_tex="analise/registro_classes.tex"):
#     """
#     Gera arquivos detalhados com as operações que provam a conjugação entre os elementos das classes.
#     Para cada par (g, h) na classe, mostra h * g * h⁻¹ = g'
#     """
#     nome_por_perm = {tuple(v): k for k, v in dicionario_perms.items()}
#     latex = ["\\begin{align*}"]
#     texto = []

#     for idx, classe in enumerate(classes, 1):
#         elementos = sorted(list(classe))
#         latex.append(f"\\text{{Classe {idx}}} \\\\")
#         texto.append(f"Classe {idx}:")

#         for g in elementos:
#             print(g)
#             print(dicionario_perms)
#             pg = dicionario_perms[g]
#             for h in elementos:
#                 ph = dicionario_perms[h]
#                 ph_inv = [ph.index(i) for i in range(len(ph))]

#                 comp1 = [ph[i] for i in pg]  # h * g
#                 conjugado = [comp1[i] for i in ph_inv]  # h * g * h⁻¹
#                 g_conj = nome_por_perm.get(tuple(conjugado), "?")

#                 texto.append(f"{h} * {g} * {h}⁻¹ = {g_conj}")
#                 latex.append(f"& {h} {g} {h}^{{-1}} = {g_conj} \\\\")

#         texto.append("")
#         latex.append("")

#     latex.append("\\end{align*}")

#     Path(destino_txt).write_text("\n".join(texto), encoding="utf-8")
#     Path(destino_tex).write_text("\n".join(latex), encoding="utf-8")

#     return destino_txt, destino_tex

def nome_para_latex(nome):
    nome = nome.replace("'", "^{\\prime}")
    nome = nome.replace("²", "^2")
    nome = nome.replace("sigma_v", "sigma_{v}")
    nome = nome.replace("sigma_d", "sigma_{d}")
    nome = nome.replace("sigma_h", "sigma_{h}")
    nome = re.sub(r"(C[2346])_\((\w)\)", r"\\mathrm{\1}^{(\2)}", nome)
    nome = re.sub(r"(C[2346])", r"\\mathrm{\1}", nome)
    nome = re.sub(r"(S[36])", r"\\mathrm{\1}", nome)
    nome = re.sub(r"\bsigma_?(v\d+)", r"\\sigma_{\1}", nome)
    nome = re.sub(r"\bsigma", r"\\sigma", nome)
    return f"${nome}$"

def salvar_classes_conjugacao(classes, path_txt="analise/classes.txt", path_tex="analise/classes.tex"):
    unicas = list({frozenset(v) for v in classes.values()})
    unicas.sort(key=lambda s: sorted(list(s))[0])

    Path("analise").mkdir(exist_ok=True)

    with open(path_txt, "w", encoding="utf-8") as f_txt:
        for idx, classe in enumerate(unicas, 1):
            f_txt.write(f"Classe {idx}: " + ", ".join(sorted(classe)) + "\n")

    with open(path_tex, "w", encoding="utf-8") as f_tex:
        f_tex.write("\\begin{itemize}\n")
        for idx, classe in enumerate(unicas, 1):
            itens = ", ".join(nome_para_latex(n) for n in sorted(classe))
            f_tex.write(f"  \\item Classe {idx}: {itens}\n")
        f_tex.write("\\end{itemize}\n")
