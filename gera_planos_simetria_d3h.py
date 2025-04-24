import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

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

def plot_plano(ax, ponto, normal, tamanho=2.0, cor='cyan', alpha=0.25, nome=None):
    d = np.array(normal, dtype=float)
    d = d / np.linalg.norm(d)
    if np.allclose(d, [0, 0, 1]):
        u = np.array([1.0, 0, 0])
    else:
        u = np.cross(d, [0, 0, 1])
        u = u / np.linalg.norm(u)
    v = np.cross(d, u)
    u = u * tamanho
    v = v * tamanho
    grid_x = np.linspace(-1, 1, 2)
    grid_y = np.linspace(-1, 1, 2)
    X, Y = np.meshgrid(grid_x, grid_y)
    plano = ponto[:, None, None] + u[:, None, None] * X + v[:, None, None] * Y
    Xp, Yp, Zp = plano
    ax.plot_surface(Xp, Yp, Zp, alpha=alpha, color=cor, edgecolor='none')
    if nome:
        offset = 1.3
        pos_label = ponto + offset * d
        ax.text(*pos_label, nome, color='black', fontsize=12, ha='center')

def visualizar_interativamente(original, transformada, titulo="Simetria", mostrar_transformado=False,
                               mostrar_sigma_h=True, mostrar_sigma_v1=True,
                               mostrar_sigma_v2=True, mostrar_sigma_v3=True):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_proj_type("ortho")

    base_colors = plt.cm.get_cmap("tab10", len(original))
    cores = [base_colors(i) for i in range(len(original))]
    tamanho = {"C": 400, "H": 300}
    deslocamento = 0.15

    for i, ((el, coord), cor) in enumerate(zip(original, cores)):
        x, y, z = coord
        ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="k", marker="o")
        ax.text(x + deslocamento, y + deslocamento, z + deslocamento, f"{i+1}",
                fontsize=11, color="black", ha="center", va="center", weight="bold")

    if mostrar_transformado:
        for i, ((el, coord), cor) in enumerate(zip(transformada, cores)):
            x, y, z = coord
            ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="r", marker="^")

    for i, (el1, c1) in enumerate(original):
        for j, (el2, c2) in enumerate(original):
            if i < j:
                dist = np.linalg.norm(np.array(c1) - np.array(c2))
                if ((el1 == "C" and el2 == "H") or (el1 == "H" and el2 == "C")) and dist < 1.2:
                    ax.plot(*zip(c1, c2), color="gray", lw=1)
                elif el1 == "C" and el2 == "C" and dist < 2.0:
                    ax.plot(*zip(c1, c2), color="black", lw=2)

    if mostrar_sigma_h:
        plot_plano(ax, np.array([0, 0, 0], dtype=float), [0, 0, 1], cor='cyan', nome=r'$\sigma_h$')
    if mostrar_sigma_v1:
        plot_plano(ax, np.array([0, 0, 0], dtype=float), [1, 0, 0], cor='lightgreen', nome=r'$\sigma_{v1}$')
    if mostrar_sigma_v2:
        plot_plano(ax, np.array([0, 0, 0], dtype=float), [np.sqrt(3), 1, 0], cor='violet', nome=r'$\sigma_{v2}$')
    if mostrar_sigma_v3:
        plot_plano(ax, np.array([0, 0, 0], dtype=float), [-np.sqrt(3), 1, 0], cor='pink', nome=r'$\sigma_{v3}$')

    ax.set_title(titulo)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python visualizador_interativo.py caminho_para_molecula.xyz")
        sys.exit(1)

    caminho_mol = sys.argv[1]
    mol = ler_xyz(caminho_mol)

    R_y = np.array([
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, -1]
    ])
    mol_rot = aplicar_rotacao(mol, R_y)

    visualizar_interativamente(mol, mol_rot, "Rotação C₂ eixo Y", mostrar_transformado=True)
    input("Pressione Enter para fechar...")
