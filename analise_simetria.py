import numpy as np
from operacoes import aplicar_operacao, aplicar_matriz
from gera_tabela_multiplicacao import *

def analiza_simetria(mol, operacoes):
    perm_dict = {}
    print("Operações disponíveis:")
    print(operacoes)
    for idx, op in enumerate(operacoes, start=1):
        desc = op.get("comentario", f"operação {idx}")
        print(f"[{idx}] {desc}")
        Rmat, destaque = aplicar_operacao(op)
        mol_transformada = aplicar_matriz(mol, Rmat)
        permutacao = obter_permutacao(mol,mol_transformada)
        print(permutacao)
        perm_dict[op["nome"]] = permutacao
    for nome, perm in perm_dict.items():
        print(f"{nome}: {perm}")
    print("*Fim*")

    dicionario_perms = perm_dict

    nomes, tabela = gerar_tabela_multiplicacao(dicionario_perms)

    with open("tabela.txt", "w") as f:
        for nome, linha in zip(nomes, tabela):
            f.write(f"{nome}: " + " ".join(linha) + "\n")

    with open("tabela.tex", "w") as f:
        f.write(gerar_tabela_latex(nomes, tabela))

    print("Tabelas geradas: tabela.txt e tabela.tex")
    return

def obter_permutacao(orig_coords, transf_coords, tol=1e-3):
    permutacao = []
    for _, coord in transf_coords:
        for i, (_, ref) in enumerate(orig_coords):
            if np.allclose(coord, ref, atol=tol):
                permutacao.append(i)
                break
        else:
            permutacao.append(None)
    return permutacao