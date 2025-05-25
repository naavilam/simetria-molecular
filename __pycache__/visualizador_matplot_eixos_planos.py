
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from render_matplot import desenhar_plano, desenhar_eixo

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
        return np.eye(3)
    elif tipo == "rotacao":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        eixo = eixo / np.linalg.norm(eixo)
        from scipy.spatial.transform import Rotation as R
        return R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()
    elif tipo == "reflexao":
        n = np.array(operacao["plano_normal"])
        n = n / np.linalg.norm(n)
        return np.eye(3) - 2 * np.outer(n, n)
    elif tipo == "impropria":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        eixo = eixo / np.linalg.norm(eixo)
        from scipy.spatial.transform import Rotation as R
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()
        plano = np.eye(3) - 2 * np.outer([0, 0, 1], [0, 0, 1])
        return plano @ rot
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")

def aplicar_matriz(molecula, Rmat):
    return [(el, Rmat @ np.array(coord)) for el, coord in molecula]

def desenhar_molecula(ax, molecula, titulo, deslocamento=0.3):
    base_colors = plt.cm.get_cmap("tab10", len(molecula))
    cores = [base_colors(i) for i in range(len(molecula))]

    tamanho = {"C": 400, "H": 300}
    for i, ((el, coord), cor) in enumerate(zip(molecula, cores)):
        x, y, z = coord
        ax.scatter(x, y, z, color=cor, s=tamanho[el], edgecolor="k", marker="o")
        ax.text(x + deslocamento, y + deslocamento, z + deslocamento, f"{i+1}",
                fontsize=11, color="black", ha="center", va="center", weight="bold")

    ax.set_title(titulo)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=45, azim=60)
    ax.set_proj_type("ortho")

def visualizar_comparacao(original, transformada, op_data, titulo="Simetria aplicada"):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')

    desenhar_molecula(ax1, original, "Antes da simetria")
    desenhar_molecula(ax2, transformada, "Depois da simetria")

    # Verifica e desenha eixo e/ou plano na visualização original
    if "eixo" in op_data:
        desenhar_eixo(ax1, op_data["eixo"])
    if "plano_normal" in op_data:
        desenhar_plano(ax1, op_data["plano_normal"])

    fig.suptitle(titulo, fontsize=14, weight="bold")
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xyz", help="Arquivo .xyz da molécula")
    parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria")
    parser.add_argument("--op", type=int, help="Índice da operação")
    args = parser.parse_args()

    mol = ler_xyz(args.xyz)

    with open(args.grupo, "r") as f:
        grupo = json.load(f)

    if args.op is None:
        print("Operações disponíveis:")
        for i, op in enumerate(grupo["operacoes"]):
            print(f"[{i}] {op.get('comentario', op['tipo'])}")
        return

    op_data = grupo["operacoes"][args.op]
    Rmat = aplicar_operacao(op_data)
    mol_transformada = aplicar_matriz(mol, Rmat)

    visualizar_comparacao(mol, mol_transformada, op_data, f"Operação: {op_data.get('comentario', '')}")

if __name__ == "__main__":
    main()
