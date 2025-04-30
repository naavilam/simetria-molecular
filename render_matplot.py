
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# def desenhar_eixo(ax, vetor, cor="blue"):
#     vetor = np.array(vetor, dtype=float)
#     vetor = vetor / np.linalg.norm(vetor)
#     ax.quiver(0, 0, 0, vetor[0], vetor[1], vetor[2],
#               color=cor, linewidth=2, arrow_length_ratio=0.15)

# def desenhar_plano(ax, normal, tamanho=2.0, cor="cyan"):
#     normal = np.array(normal, dtype=float)
#     normal = normal / np.linalg.norm(normal)

#     if np.allclose(normal, [0, 0, 1]):
#         v = np.array([1, 0, 0], dtype=float)
#     else:
#         v = np.cross(normal, [0, 0, 1])
#         v = np.array(v, dtype=float)
#         v = v / np.linalg.norm(v)

#     w = np.cross(normal, v)
#     w = np.array(w, dtype=float)

#     v *= tamanho
#     w *= tamanho
#     centro = np.array([0, 0, 0], dtype=float)

#     p = np.array([
#         centro - v - w,
#         centro - v + w,
#         centro + v + w,
#         centro + v - w
#     ])

#     ax.add_collection3d(Poly3DCollection([p], color=cor, alpha=0.3))

# def desenhar_molecula(ax, molecula, titulo, tamanho, deslocamento=0.3, destaque=None):
#     base_colors = plt.cm.get_cmap("tab10", len(molecula))
#     cores = [base_colors(i) for i in range(len(molecula))]

#     tamanho = {"C": 400, "H": 300}
#     for i, ((el, coord), cor) in enumerate(zip(molecula, cores)):
#         x, y, z = coord
#         ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="k", marker="o")
#         ax.text(x + deslocamento, y + deslocamento, z + deslocamento, f"{i+1}",
#                 fontsize=11, color="black", ha="center", va="center", weight="bold")

#     ax.set_title(titulo)
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.set_zticks([])
#     ax.set_axis_off()
#     ax.set_box_aspect([1, 1, 1])
#     ax.view_init(elev=45, azim=60)
#     ax.set_proj_type("ortho")



def desenhar_molecula(ax, molecula, titulo, tamanho, deslocamento=0.2, destaque=None):
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

    if destaque is not None:
        if isinstance(destaque, list):
            for tipo, vetor in destaque:
                if tipo == "eixo":
                    desenhar_eixo(ax, vetor)
                elif tipo == "plano":
                    desenhar_plano(ax, vetor)
        else:
            tipo, vetor = destaque
            if tipo == "eixo":
                desenhar_eixo(ax, vetor)
            elif tipo == "plano":
                desenhar_plano(ax, vetor)

    ax.set_title(titulo)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=45, azim=60)
    ax.set_proj_type("ortho")

def desenhar_eixo(ax, vetor, cor="blue"):
    vetor = np.array(vetor)
    vetor = vetor / np.linalg.norm(vetor)
    ax.quiver(0, 0, 0, vetor[0], vetor[1], vetor[2],
              color=cor, linewidth=2, arrow_length_ratio=0.15)

def desenhar_plano(ax, normal, tamanho=2.0, cor="cyan"):
    normal = np.array(normal, dtype=float)
    normal = normal / np.linalg.norm(normal)

    # Encontrar dois vetores ortogonais ao vetor normal
    if np.allclose(normal, [0, 0, 1]):
        v = np.array([1, 0, 0], dtype=float)
    else:
        v = np.cross(normal, [0, 0, 1])
        v = np.array(v, dtype=float)  # <-- cast explícito
        v = v / np.linalg.norm(v)

    w = np.cross(normal, v)
    w = np.array(w, dtype=float)  # <-- cast explícito

    v *= tamanho
    w *= tamanho
    centro = np.array([0, 0, 0], dtype=float)

    # Quatro cantos do plano
    p = np.array([
        centro - v - w,
        centro - v + w,
        centro + v + w,
        centro + v - w
    ])

    # Criar um polígono 3D translúcido
    ax.add_collection3d(Poly3DCollection([p], color=cor, alpha=0.3))


def visualizar_matplot(original, transformada, titulo="Simetria aplicada", destaque=None):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    tamanho = {"C": 400, "H": 300}
    desenhar_molecula(ax1, original, "Antes da simetria", tamanho, destaque=destaque)
    desenhar_molecula(ax2, transformada, "Depois da simetria", tamanho, destaque=destaque)
    fig.suptitle(titulo, fontsize=14, weight="bold")
    plt.tight_layout()
    plt.show()

