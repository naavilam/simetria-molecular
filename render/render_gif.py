"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-05-25                                                                **
**                                                      License: Custom Attribution License                                                       **
**                                                                                                                                                **
**    Este módulo faz parte do projeto de simetria molecular desenvolvido no contexto da disciplina de pós-graduação PGF5261 Teoria de Grupos     **
**                                                       Aplicada para Sólidos e Moléculas.                                                       **
**                                                                                                                                                **
**   Permission is granted to use, copy, modify, and distribute this file, provided that this notice is retained in full and that the origin of   **
**    the software is clearly and explicitly attributed to the original author. Such attribution must be preserved not only within the source     **
**       code, but also in any accompanying documentation, public display, distribution, or derived work, in both digital or printed form.        **
**                                                  For licensing inquiries: contact@chanah.dev                                                   **
====================================================================================================================================================
"""

import pyvista as pv
import imageio.v2 as imageio
import numpy as np
import json
import os
from pathlib import Path

class SimetriaAnimada:

    """Description
    
    Attributes:
        coords (TYPE): Description
        frame_count (int): Description
        gif_name (TYPE): Description
        json_path (TYPE): Description
        operacoes (TYPE): Description
        output_dir (TYPE): Description
        xyz_path (TYPE): Description
    """
    
    def __init__(self, xyz_path, json_path, output_dir="frames_animados", gif_name="simetria_animada.gif"):
        self.xyz_path = xyz_path
        self.json_path = json_path
        self.output_dir = Path(output_dir)
        self.gif_name = gif_name
        self.coords = self.ler_xyz()
        self.operacoes = self.ler_operacoes()
        self.frame_count = 0
        self.output_dir.mkdir(exist_ok=True)

    def ler_xyz(self):
        """Description
        
        Returns:
            TYPE: Description
        """
        with open(self.xyz_path) as f:
            linhas = f.readlines()[2:]
        coords = [list(map(float, linha.split()[1:4])) for linha in linhas]
        return np.array(coords)

    def ler_operacoes(self):
        """Description
        
        Returns:
            TYPE: Description
        """
        with open(self.json_path) as f:
            data = json.load(f)
        return data["operacoes"]

    def rotacao_matriz(self, eixo, angulo_rad):
        """Description
        
        Args:
            eixo (TYPE): Description
            angulo_rad (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        eixo = eixo / np.linalg.norm(eixo)
        ux, uy, uz = eixo
        cos = np.cos(angulo_rad)
        sin = np.sin(angulo_rad)
        return np.array([
            [cos + ux**2 * (1 - cos), ux*uy*(1 - cos) - uz*sin, ux*uz*(1 - cos) + uy*sin],
            [uy*ux*(1 - cos) + uz*sin, cos + uy**2 * (1 - cos), uy*uz*(1 - cos) - ux*sin],
            [uz*ux*(1 - cos) - uy*sin, uz*uy*(1 - cos) + ux*sin, cos + uz**2 * (1 - cos)]
        ])

    def aplicar_rotacao_interpolada(self, eixo, angulo_total, steps=10):
        """Description
        
        Args:
            eixo (TYPE): Description
            angulo_total (TYPE): Description
            steps (int, optional): Description
        
        Returns:
            TYPE: Description
        """
        frames = []
        for i in range(steps + 1):
            theta = angulo_total * i / steps
            R = self.rotacao_matriz(eixo, theta)
            frames.append(self.coords @ R.T)
        return frames

    def aplicar_reflexao_interpolada(self, plano_normal, steps=10):
        """Description
        
        Args:
            plano_normal (TYPE): Description
            steps (int, optional): Description
        
        Returns:
            TYPE: Description
        """
        plano_normal = plano_normal / np.linalg.norm(plano_normal)
        refletido = self.coords - 2 * np.outer(self.coords @ plano_normal, plano_normal)
        return [(1 - alpha) * self.coords + alpha * refletido for alpha in np.linspace(0, 1, steps + 1)]

    def desenhar_molecula(self, plotter, coords, cor='gray'):
        """Description
        
        Args:
            plotter (TYPE): Description
            coords (TYPE): Description
            cor (str, optional): Description
        """
        for ponto in coords:
            esfera = pv.Sphere(radius=0.2, center=ponto)
            plotter.add_mesh(esfera, color=cor, show_edges=False)

    def gerar_frames(self):
        """Description
        """
        for op in self.operacoes:
            tipo = op.get("tipo")
            if tipo == "identidade":
                continue

            if tipo in ("rotacao", "impropria"):
                eixo = np.array(op["eixo"], float)
                angulo = np.radians(op["angulo"])
                frames = self.aplicar_rotacao_interpolada(eixo, angulo)
            elif tipo == "reflexao":
                plano = np.array(op["plano_normal"], float)
                frames = self.aplicar_reflexao_interpolada(plano)
            else:
                continue

            for frame_coords in frames:
                plotter = pv.Plotter(off_screen=True)
                self.desenhar_molecula(plotter, self.coords, cor='gray')
                self.desenhar_molecula(plotter, frame_coords, cor='blue')
                filename = self.output_dir / f"frame_{self.frame_count:03d}.png"
                plotter.screenshot(str(filename))
                plotter.close()
                self.frame_count += 1

    def gerar_gif(self):
        """Description
        """
        imagens = [self.output_dir / f"frame_{i:03d}.png" for i in range(self.frame_count)]
        with imageio.get_writer(self.gif_name, mode="I", duration=0.1) as writer:
            for imagem in imagens:
                writer.append_data(imageio.imread(imagem))

    def executar(self):
        """Description
        """
        self.gerar_frames()
        self.gerar_gif()
        print(f"GIF animado gerado: {self.gif_name}")