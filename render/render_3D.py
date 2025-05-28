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
import numpy as np

class PyvistaVisualizer:
    
    def __init__(self, original, transformada, titulo="Simetria aplicada", destaque=None, cores=None):
        self.original = original
        self.transformada = transformada
        self.titulo = titulo
        self.destaque = destaque
        self.tamanho = {"C": 0.3, "H": 0.2}
        self.cores_personalizadas = cores
        self.plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))

    def renderizar(self):
        self.plotter.subplot(0, 0)
        self._desenhar_molecula(self.original, "Antes da simetria", self.destaque)

        self.plotter.subplot(0, 1)
        self._desenhar_molecula(self.transformada, "Depois da simetria")

        self.plotter.add_text(self.titulo, position="upper_edge", font_size=14, color="black")
        self.plotter.link_views()
        self.plotter.camera.azimuth -= 25
        self.plotter.camera.elevation -= 20
        self.plotter.camera.roll += 1
        self.plotter.show()

    def _desenhar_molecula(self, molecula, title, destaque=None):
        # self.plotter.add_text(title, font_size=12) # e novo?
        cores = self._gerar_cores(len(molecula))
        self._desenhar_atomicos(molecula, cores)
        self._numerar_atomicos(molecula)
        self._desenhar_ligacoes(molecula)
        if destaque:
            self._destacar(destaque)

    def _gerar_cores(self, n):
        if self.cores_personalizadas:
            return self.cores_personalizadas[:n]
        base = [
            (174, 198, 207), (255, 179, 71), (179, 158, 181),
            (119, 221, 119), (255, 105, 97), (253, 253, 150),
            (207, 207, 196), (244, 154, 194), (222, 165, 164),
            (176, 224, 230), (230, 230, 250), (197, 227, 132)
        ]
        return base[:n]

    def _desenhar_atomicos(self, molecula, cores):
        for i, (el, coord) in enumerate(molecula.como_tuplas()):
            cor = cores[i % len(cores)]
            raio = self.tamanho.get(el, 0.2)
            esfera = pv.Sphere(radius=raio, center=coord)
            self.plotter.add_mesh(esfera, color=cor, smooth_shading=True)

    def _numerar_atomicos(self, molecula):
        for idx, (_, coord) in enumerate(molecula.como_tuplas(), start=1):
            self.plotter.add_point_labels(
                [coord], [str(idx)],
                font_size=14, text_color='white',
                point_size=0, shape_opacity=0, always_visible=True
            )

    def _desenhar_ligacoes(self, molecula):
        coords = molecula.como_tuplas()
        for i, (_, c1) in enumerate(coords):
            for j, (_, c2) in enumerate(coords):
                if i < j:
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    if dist < 1.2:
                        self.plotter.add_mesh(pv.Line(c1, c2), color="gray", line_width=3)

        for i, (el1, c1) in enumerate(coords):
            for j, (el2, c2) in enumerate(coords):
                if i < j and el1 == 'C' and el2 == 'C':
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    if dist < 1.6:
                        self.plotter.add_mesh(pv.Line(c1, c2), color='black', line_width=4)
    
    def _destacar(self, destaque):
        destaques = destaque if isinstance(destaque, list) else [destaque]
        for d in destaques:
            tipo = d["tipo"]
            centro = np.array(d.get("origem", [0.0, 0.0, 0.0]))

            if tipo == "eixo":
                mesh = self._gerar_eixo(d, centro)
                self.plotter.add_mesh(mesh, color="gray", line_width=3)

            elif tipo == "plano":
                mesh = self._gerar_plano(d, centro)
                self.plotter.add_mesh(mesh, color="gray", opacity=0.3, show_edges=False)

            elif tipo == "ponto":
                mesh = self._gerar_ponto(centro)
                self.plotter.add_mesh(mesh, color="gray", opacity=0.5)

            else:
                print(f"[AVISO] Tipo de destaque desconhecido: {tipo}")

    def _gerar_eixo(self, d, centro):
        vetor = np.array(d["direcao"])
        vetor /= np.linalg.norm(vetor)
        return pv.Line(
            pointa=centro - 3.0 * vetor,
            pointb=centro + 3.0 * vetor,
            resolution=1
        )

    def _gerar_plano(self, d, centro):
        normal = np.array(d["normal"])
        return pv.Plane(
            center=centro,
            direction=normal / np.linalg.norm(normal),
            i_size=4.0,
            j_size=4.0
        )

    def _gerar_ponto(self, centro):
        return pv.Sphere(radius=0.1, center=centro)