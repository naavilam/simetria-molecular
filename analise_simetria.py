import numpy as np
from gera_permutacoes import detalhe_operacao, aplicar_matriz
from gera_tabela_multiplicacao import gerar_tabela_multiplicacao
from gera_classes_conjugacao import gerar_classe_conjugacao

def analiza_simetria(mol, operacoes):
    perm_dict = {}
    for idx, op in enumerate(operacoes, start=1):
        desc = op.get("comentario", f"operação {idx}")
        print(f"[{idx}] {desc}")
        Rmat, destaque = detalhe_operacao(op)
        mol_transformada = aplicar_matriz(mol, Rmat)
        permutacao = obter_permutacao(mol,mol_transformada)
        perm_dict[op["nome"]] = permutacao
    print("*****************Operações Básicas*****************")
    for nome, perm in perm_dict.items():
        print(f"{nome}: {perm}")
    print("********Fim da Analise das Operações Básicas*******")

    dicionario_perms = perm_dict

    tab_mult = gerar_tabela_multiplicacao(dicionario_perms)
    gerar_classe_conjugacao(dicionario_perms, tab_mult)
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