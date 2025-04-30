import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

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

def plotar_molecula_com_estilo(original, transformada, titulo="Simetria aplicada", mostrar_transformado=False, salvar_em=None):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
    ax.set_proj_type('ortho')

    base_colors = plt.cm.get_cmap("tab10", len(original))
    cores = [base_colors(i) for i in range(len(original))]
    tamanho = {"C": 100, "H": 60}

    for i, ((el, coord), cor) in enumerate(zip(original, cores)):
        x, y, z = coord
        ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="k", marker="o", zorder=3)
        ax.text(x, y, z, f"{el}{i}", fontsize=8, zorder=4)

    if mostrar_transformado:
        for i, ((el, coord), cor) in enumerate(zip(transformada, cores)):
            x, y, z = coord
            ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="r", marker="^", zorder=2)

    for i, (el1, c1) in enumerate(original):
        for j, (el2, c2) in enumerate(original):
            if i < j:
                dist = np.linalg.norm(np.array(c1) - np.array(c2))
                if ((el1 == "C" and el2 == "H") or (el1 == "H" and el2 == "C")) and dist < 1.2:
                    ax.plot(*zip(c1, c2), color="gray", lw=1, zorder=1)
                elif el1 == "C" and el2 == "C" and dist < 2.0:
                    ax.plot(*zip(c1, c2), color="black", lw=2, zorder=1)

    ax.quiver(0, 0, 0, 1.2, 0, 0, color="r", arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, 1.2, 0, color="g", arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, 0, 1.2, color="b", arrow_length_ratio=0.08)
    ax.text(1.3, 0, 0, "X", color="r")
    ax.text(0, 1.3, 0, "Y", color="g")
    ax.text(0, 0, 1.3, "Z", color="b")

    ax.set_title(titulo)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    plt.tight_layout()

    if salvar_em:
        os.makedirs(os.path.dirname(salvar_em), exist_ok=True)
        plt.savefig(salvar_em, dpi=300)
        print(f"Imagem salva em: {salvar_em}")
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python visualizador.py caminho_para_molecula.xyz")
        sys.exit(1)

    caminho_mol = sys.argv[1]
    mol = ler_xyz(caminho_mol)

    # Exemplo de operação: rotação C2 em Y
    R_y = np.array([
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, -1]
    ])
    mol_rot = aplicar_rotacao(mol, R_y)

    salvar_path = f"imagens/C2_y_{os.path.basename(caminho_mol).replace('.xyz','')}.png"
    plotar_molecula_com_estilo(mol, mol_rot, "Rotação C₂ eixo Y", mostrar_transformado=False, salvar_em=salvar_path)

