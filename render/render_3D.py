"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-06-14                                                                **
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

from .render import Renderer
import pyvista as pv
import numpy as np

class MoleculeExplorer(Renderer):

    """Summary
    """

    def __init__(self, molecula, grupo):
        self.molecula = molecula
        self.grupo = grupo
        self.titulo = "Visualizador de Simetria 3D"
        self.tamanho = {"C": 0.3, "H": 0.2}
        self.plotter = pv.Plotter(window_size=(1200, 800))
        self.operacoes = {op["id"]: op for op in grupo.operacoes}  # Mapa id -> operação

    def render(self, resultados: dict) -> str:
        self._desenhar_molecula(self.molecula)
        self.plotter.add_text(self.titulo, position="upper_edge", font_size=14, color="black")

        # Criar um botão para cada operação do grupo
        for op_id, operacao in self.operacoes.items():
            label = operacao.get("comentario") or operacao.get("nome") or f"Op {op_id}"
            self.plotter.add_button_widget(
                lambda op_id=op_id: self._aplicar_operacao(op_id),
                label=label,
                position=None,
                color_on='white',
                font_size=12
            )

        self.plotter.show()
        return "Renderização exibida no servidor (local)"

    def _desenhar_molecula(self, molecula):
        cores = self._gerar_cores(len(molecula))
        self._desenhar_atomicos(molecula, cores)
        self._numerar_atomicos(molecula)
        self._desenhar_ligacoes(molecula)

    def _gerar_cores(self, n):
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
                if i < j and coords[i][0] == 'C' and coords[j][0] == 'C':
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    if dist < 1.6:
                        self.plotter.add_mesh(pv.Line(c1, c2), color='black', line_width=4)

    def _aplicar_operacao(self, op_id):
        operacao = self.operacoes[op_id]
        print(f"Aplicando operação: {operacao.get('nome')}")

        # Aqui você pode implementar a aplicação real da operação sobre self.molecula
        # Exemplo: aplicar uma rotação, reflexão, etc, conforme o conteúdo do JSON do grupo.
        # Por enquanto só exemplo de print para teste:
        # TODO: implementar transformação geométrica real