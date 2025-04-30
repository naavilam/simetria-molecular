
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def plotar_molecula_com_ligacoes(original, transformada, titulo="Comparação com linhas de ligação"):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    cor = {"C": "black", "H": "skyblue"}
    tamanho = {"C": 100, "H": 60}

    coords_orig = [(el, np.array(coord)) for el, coord in original]
    coords_rot = [(el, np.array(coord)) for el, coord in transformada]

    for i, (el, coord) in enumerate(coords_orig):
        x, y, z = coord
        ax.scatter(x, y, z, c=cor[el], s=tamanho[el], edgecolor="k", marker="o")
        ax.text(x, y, z, f"{el}{i}", fontsize=8)

    for i, (el, coord) in enumerate(coords_rot):
        x, y, z = coord
        ax.scatter(x, y, z, c=cor[el], s=tamanho[el], edgecolor="r", marker="^")

    # Ligações
    for i, (el1, c1) in enumerate(coords_orig):
        for j, (el2, c2) in enumerate(coords_orig):
            if i < j:
                dist = np.linalg.norm(c1 - c2)
                if ((el1 == "C" and el2 == "H") or (el1 == "H" and el2 == "C")) and dist < 1.2:
                    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], [c1[2], c2[2]], c="gray", lw=1)
                elif el1 == "C" and el2 == "C" and dist < 2.0:
                    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], [c1[2], c2[2]], c="black", lw=2)

    # Eixos
    ax.quiver(0, 0, 0, 1.5, 0, 0, color="r", arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1.5, 0, color="g", arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1.5, color="b", arrow_length_ratio=0.1)
    ax.text(1.6, 0, 0, "X", color="r")
    ax.text(0, 1.6, 0, "Y", color="g")
    ax.text(0, 0, 1.6, "Z", color="b")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(titulo)
    ax.set_box_aspect([1, 1, 1])
    ax.set_proj_type('ortho')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    mol = ler_xyz("moleculas/etano_eclipsado.xyz")
    R_y = np.array([
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, -1]
    ])
    mol_rot = aplicar_rotacao(mol, R_y)
    plotar_molecula_com_ligacoes(mol, mol_rot, "Rotação C₂ (eixo Y) com ligações")
