import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

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
        plano = np.eye(3) - 2 * np.outer(eixo, eixo)
        return plano @ rot, eixo
    elif tipo == "inversao":
        return -np.eye(3), None
    else:
        raise ValueError(f"Operação desconhecida: {tipo}")

def aplicar_transformacao(molecula, Rmat):
    return [(el, Rmat @ np.array(coord)) for el, coord in molecula]

def plotar_molecula(ax, molecula, cor='k', marcador='o', label_prefix=""):
    tamanho = {"C": 200, "H": 120}
    for i, (el, coord) in enumerate(molecula):
        x, y, z = coord
        ax.scatter(x, y, z, color=cor, s=tamanho.get(el, 100), edgecolor="k", marker=marcador)
        ax.text(x, y, z, f"{label_prefix}{i+1}", fontsize=8, color=cor)

def desenhar_plano(ax, normal, cor='cyan'):
    normal = np.array(normal, dtype=float)
    normal = normal / np.linalg.norm(normal)
    if np.allclose(normal, [0, 0, 1]):
        u = np.array([1, 0, 0])
    else:
        u = np.cross(normal, [0, 0, 1])
        u = u / np.linalg.norm(u)
    v = np.cross(normal, u)
    u *= 2
    v *= 2
    grid = np.linspace(-1, 1, 2)
    X, Y = np.meshgrid(grid, grid)
    ponto = np.array([0, 0, 0])
    plano = ponto[:, None, None] + u[:, None, None] * X + v[:, None, None] * Y
    ax.plot_surface(*plano, alpha=0.3, color=cor, edgecolor='none')

def desenhar_eixo(ax, eixo, cor='magenta'):
    eixo = np.array(eixo)
    eixo = eixo / np.linalg.norm(eixo)
    start = -1.5 * eixo
    end = 1.5 * eixo
    ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color=cor, lw=2)

def visualizar_simetria(molecula, operacao, indice):
    Rmat, direcao = aplicar_operacao(operacao)
    transformada = aplicar_transformacao(molecula, Rmat)

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_proj_type("ortho")
    plotar_molecula(ax, molecula, cor='blue', marcador='o', label_prefix="O")
    plotar_molecula(ax, transformada, cor='red', marcador='^', label_prefix="T")

    if operacao["tipo"] == "reflexao":
        desenhar_plano(ax, direcao, cor='cyan')
    elif operacao["tipo"] in ["rotacao", "impropria"]:
        desenhar_eixo(ax, direcao, cor='orange')

    ax.set_title(f"{indice+1}. {operacao['tipo'].capitalize()} - {operacao.get('comentario', '')}")
    ax.set_box_aspect([1,1,1])
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Visualizador genérico de simetria molecular")
    parser.add_argument("xyz", help="Arquivo .xyz da molécula")
    parser.add_argument("grupo", help="Arquivo .json com grupo de simetria")
    parser.add_argument("--indice", type=int, help="Índice da operação a visualizar (1-based)")
    args = parser.parse_args()

    molecula = ler_xyz(args.xyz)

    with open(args.grupo, 'r') as f:
        grupo = json.load(f)
    operacoes = grupo["operacoes"]

    if args.indice is not None:
        indice = args.indice-1
        visualizar_simetria(molecula, operacoes[indice], indice)
    else:
        print("Operações disponíveis:")
        for i, op in enumerate(operacoes):
            print(f"{i+1}. {op['tipo']} - {op.get('comentario', '')}")

if __name__ == "__main__":
    main()
