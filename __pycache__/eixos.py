
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.ion()

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

def aplicar_rotacao(molecula, Rmat):
    return [(el, Rmat @ np.array(coord)) for el, coord in molecula]

def desenhar_molecula(ax, molecula, titulo, tamanho, deslocamento=0.1):
    base_colors = plt.cm.get_cmap("tab10", len(molecula))
    cores = [base_colors(i) for i in range(len(molecula))]

    for i, ((el, coord), cor) in enumerate(zip(molecula, cores)):
        x, y, z = coord
        ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="k", marker="o")
        ax.text(x + deslocamento, y + deslocamento, z + deslocamento, f"{i+1}",
                fontsize=11, color="black", ha="center", va="center", weight="bold")

    for i, (el1, c1) in enumerate(molecula):
        for j, (el2, c2) in enumerate(molecula):
            if i < j:
                dist = np.linalg.norm(np.array(c1) - np.array(c2))
                if ((el1 == "C" and el2 == "H") or (el1 == "H" and el2 == "C")) and dist < 1.2:
                    ax.plot(*zip(c1, c2), color="gray", lw=1)
                elif el1 == "C" and el2 == "C" and dist < 2.0:
                    ax.plot(*zip(c1, c2), color="black", lw=2)

def desenhar_eixo(ax, origem, vetor, nome, cor, comprimento=2.0):
    v = np.array(vetor) / np.linalg.norm(vetor)
    destino = origem + v * comprimento
    ax.plot([origem[0], destino[0]], [origem[1], destino[1]], [origem[2], destino[2]],
            color=cor, linestyle='dashed', linewidth=2)
    label_pos = origem + v * (comprimento + 0.2)
    ax.text(*label_pos, nome, color=cor, fontsize=12)

def visualizar_comparacao(original, transformada, titulo="Simetria aplicada",
                          mostrar_C3=True, mostrar_C2a=True, mostrar_C2b=True, mostrar_C2c=True):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    ax1.set_proj_type("ortho")
    ax2.set_proj_type("ortho")

    tamanho = {"C": 400, "H": 300}
    desenhar_molecula(ax1, original, "Antes da simetria", tamanho)
    desenhar_molecula(ax2, transformada, "Depois da simetria", tamanho)

    if mostrar_C3:
        desenhar_eixo(ax1, np.array([0, 0, 0]), [0, 0, 1], "C₃", "blue")
        desenhar_eixo(ax2, np.array([0, 0, 0]), [0, 0, 1], "C₃", "blue")

    if mostrar_C2a:
        desenhar_eixo(ax1, np.array([0, 0, 0]), [1, 0, 0], "C₂(a)", "green")
        desenhar_eixo(ax2, np.array([0, 0, 0]), [1, 0, 0], "C₂(a)", "green")

    if mostrar_C2b:
        desenhar_eixo(ax1, np.array([0, 0, 0]), [-0.5, np.sqrt(3)/2, 0], "C₂(b)", "orange")
        desenhar_eixo(ax2, np.array([0, 0, 0]), [-0.5, np.sqrt(3)/2, 0], "C₂(b)", "orange")

    if mostrar_C2c:
        desenhar_eixo(ax1, np.array([0, 0, 0]), [-0.5, -np.sqrt(3)/2, 0], "C₂(c)", "purple")
        desenhar_eixo(ax2, np.array([0, 0, 0]), [-0.5, -np.sqrt(3)/2, 0], "C₂(c)", "purple")

    fig.suptitle(titulo, fontsize=14, weight="bold")
    for ax in [ax1, ax2]:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_axis_off()
        ax.set_box_aspect([1, 1, 1])
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

if __name__ == "__main__":
    mol = ler_xyz("moleculas/etano_eclipsado.xyz")
    R_y = np.array([
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, -1]
    ])
    mol_rot = aplicar_rotacao(mol, R_y)
    visualizar_comparacao(mol, mol_rot,
        titulo="Rotação C₂ eixo Y",
        mostrar_C3=True,
        mostrar_C2a=True,
        mostrar_C2b=True,
        mostrar_C2c=True
    )
    input("Pressione Enter para fechar...")
