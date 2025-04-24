
import numpy as np
from scipy.spatial.transform import Rotation as R
import json
from itertools import permutations
from typing import List, Tuple
import sys

TOL = 1e-1

def carregar_grupo_json(path_json):
    with open(path_json, 'r') as f:
        dados = json.load(f)
    return dados["operacoes"]

def aplicar_operacao(operacao):
    tipo = operacao["tipo"]
    if tipo == "identidade":
        return np.eye(3)
    elif tipo == "rotacao":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        return R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
    elif tipo == "reflexao":
        n = np.array(operacao["plano_normal"])
        n = n / np.linalg.norm(n)
        return np.eye(3) - 2 * np.outer(n, n)
    elif tipo == "impropria":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
        normal = eixo / np.linalg.norm(eixo)
        reflexao = np.eye(3) - 2 * np.outer(normal, normal)
        return reflexao @ rot
    else:
        raise ValueError(f"Tipo de operação desconhecido: {tipo}")

def aplicar_transformacao(molecula, Rmat):
    return [(elem, Rmat @ np.array(coord)) for elem, coord in molecula]

def compara_completa(orig, rot, tipo="todos"):
    if tipo == "H":
        orig_coords = [np.array(coord) for elem, coord in orig if elem == "H"]
        rot_coords = [np.array(coord) for elem, coord in rot if elem == "H"]
    else:
        orig_coords = [np.array(coord) for _, coord in orig]
        rot_coords = [np.array(coord) for _, coord in rot]
    for perm in permutations(rot_coords):
        if all(np.linalg.norm(a - b) < TOL for a, b in zip(orig_coords, perm)):
            return True
    return False

def ler_xyz(path):
    with open(path, 'r') as f:
        linhas = f.readlines()
    natomos = int(linhas[0])
    molecula = []
    for linha in linhas[2:2+natomos]:
        partes = linha.split()
        elemento = partes[0]
        coords = list(map(float, partes[1:4]))
        molecula.append((elemento, coords))
    return molecula

def detectar_simetrias_com_comentarios(molecula, path_json, tipo_comparacao="todos"):
    operacoes = carregar_grupo_json(path_json)
    simetrias_validas = []
    for operacao in operacoes:
        Rmat = aplicar_operacao(operacao)
        mol_transformada = aplicar_transformacao(molecula, Rmat)
        if compara_completa(molecula, mol_transformada, tipo=tipo_comparacao):
            simetrias_validas.append(operacao.get("comentario", "operação sem descrição"))
    return simetrias_validas

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 simetrias_etano_comentado.py caminho_entrada.xyz grupo.json")
        sys.exit(1)

    caminho_mol = sys.argv[1]
    caminho_grupo = sys.argv[2]

    mol = ler_xyz(caminho_mol)
    simetrias = detectar_simetrias_com_comentarios(mol, caminho_grupo, tipo_comparacao="todos")

    print(f"Simetrias detectadas para {caminho_mol} com base no grupo {caminho_grupo}:\n")
    for i, s in enumerate(simetrias, 1):
        print(f"{i}. {s}")
