import pyvista as pv
import imageio.v2 as imageio
import numpy as np
import json
import os
import sys

def ler_xyz(path):
    with open(path) as f:
        linhas = f.readlines()[2:]
    coords = [list(map(float, linha.split()[1:4])) for linha in linhas]
    return np.array(coords)

def rotacao_matriz(eixo, angulo_rad):
    eixo = eixo / np.linalg.norm(eixo)
    ux, uy, uz = eixo
    cos = np.cos(angulo_rad)
    sin = np.sin(angulo_rad)
    return np.array([
        [cos + ux**2 * (1 - cos), ux*uy*(1 - cos) - uz*sin, ux*uz*(1 - cos) + uy*sin],
        [uy*ux*(1 - cos) + uz*sin, cos + uy**2 * (1 - cos), uy*uz*(1 - cos) - ux*sin],
        [uz*ux*(1 - cos) - uy*sin, uz*uy*(1 - cos) + ux*sin, cos + uz**2 * (1 - cos)]
    ])

def aplicar_rotacao_interpolada(coords, eixo, angulo_total, steps):
    frames = []
    for i in range(steps + 1):
        theta = angulo_total * i / steps
        R = rotacao_matriz(eixo, theta)
        frames.append(coords @ R.T)
    return frames

def aplicar_reflexao_interpolada(coords, plano_normal, steps):
    plano_normal = plano_normal / np.linalg.norm(plano_normal)
    refletido = coords - 2 * np.outer(coords @ plano_normal, plano_normal)
    frames = [(1 - alpha) * coords + alpha * refletido for alpha in np.linspace(0, 1, steps + 1)]
    return frames

def desenhar_molecula(plotter, coords, cor='gray'):
    for ponto in coords:
        esfera = pv.Sphere(radius=0.2, center=ponto)
        plotter.add_mesh(esfera, color=cor, show_edges=False)

def main():
    if len(sys.argv) < 3:
        print("Uso: python script_gif_final.py molecula.xyz operacoes.json")
        return

    xyz_path = sys.argv[1]
    json_path = sys.argv[2]

    with open(json_path) as f:
        data = json.load(f)
        operacoes = data["operacoes"]

    coords = ler_xyz(xyz_path)
    os.makedirs("frames_animados", exist_ok=True)
    frame_count = 0

    for idx, op in enumerate(operacoes):
        tipo = op.get("tipo")
        if tipo == "identidade":
            continue

        if tipo in ("rotacao", "impropria"):
            eixo = np.array(op["eixo"], float)
            angulo = np.radians(op["angulo"])
            frames = aplicar_rotacao_interpolada(coords, eixo, angulo, steps=10)
        elif tipo == "reflexao":
            plano = np.array(op["plano_normal"], float)
            frames = aplicar_reflexao_interpolada(coords, plano, steps=10)
        else:
            continue

        for frame_coords in frames:
            plotter = pv.Plotter(off_screen=True)
            desenhar_molecula(plotter, coords, cor='gray')
            desenhar_molecula(plotter, frame_coords, cor='blue')
            plotter.screenshot(f"frames_animados/frame_{frame_count:03d}.png")
            plotter.close()
            frame_count += 1

    imagens = [f"frames_animados/frame_{i:03d}.png" for i in range(frame_count)]
    with imageio.get_writer("simetria_animada.gif", mode="I", duration=0.1) as writer:
        for imagem in imagens:
            writer.append_data(imageio.imread(imagem))

    print("GIF animado gerado: simetria_animada.gif")

if __name__ == "__main__":
    main()
