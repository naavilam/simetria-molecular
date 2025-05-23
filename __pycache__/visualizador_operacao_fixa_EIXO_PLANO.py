
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
from render_matplot import desenhar_molecula

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

def aplicar_operacao(operacao):
    tipo = operacao["tipo"]
    if tipo == "identidade":
        return np.eye(3), None
    elif tipo == "rotacao":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        eixo = eixo / np.linalg.norm(eixo)
        return R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix(), eixo
    elif tipo == "reflexao":
        n = np.array(operacao["plano_normal"])
        n = n / np.linalg.norm(n)
        return np.eye(3) - 2 * np.outer(n, n), n
    elif tipo == "impropria":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        eixo = eixo / np.linalg.norm(eixo)
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()
        plano = np.eye(3) - 2 * np.outer([0, 0, 1], [0, 0, 1])
        return plano @ rot, eixo
    else:
        raise ValueError(f"Tipo de operação desconhecido: {tipo}")

def aplicar_matriz(molecula, Rmat):
    return [(el, Rmat @ np.array(coord)) for el, coord in molecula]

def visualizar_comparacao(original, transformada, titulo="Simetria aplicada", destaque=None):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    tamanho = {"C": 400, "H": 300}
    desenhar_molecula(ax1, original, "Antes da simetria", tamanho, destaque=destaque)
    desenhar_molecula(ax2, transformada, "Depois da simetria", tamanho, destaque=destaque)
    fig.suptitle(titulo, fontsize=14, weight="bold")
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xyz", help="Arquivo .xyz da molécula")
    parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria (campo 'operacoes' é lista)")
    parser.add_argument("--op", type=int, default=None, help="Índice da operação de simetria")
    args = parser.parse_args()

    mol = ler_xyz(args.xyz)

    with open(args.grupo, "r") as f:
        grupo = json.load(f)

    operacoes = grupo["operacoes"]

    if args.op is None:
        print("Operações disponíveis:")
        for i, op in enumerate(operacoes):
            desc = op.get("comentario", f"{op['tipo']} op")
            print(f"[{i+1}] {desc}")
        return

    op = operacoes[args.op-1]
    desc = op.get("comentario", f"{op['tipo']} operação")
    Rmat, vetor_destaque = aplicar_operacao(op)

    destaque = []

    if op["tipo"] == "rotacao":
        destaque = [("eixo", vetor_destaque)]
    elif op["tipo"] == "reflexao":
        destaque = [("plano", vetor_destaque)]
    elif op["tipo"] == "impropria":
        # Operações impróprias têm eixo + plano
        destaque = [
            ("eixo", vetor_destaque),
            ("plano", np.array([0, 0, 1]))  # assumindo plano xy para D3h
        ]

    # Caso não haja nada:
    if not destaque:
        destaque = None


    mol_transformada = aplicar_matriz(mol, Rmat)
    visualizar_comparacao(mol, mol_transformada, f"Operação: {desc}", destaque)

if __name__ == "__main__":
    main()
