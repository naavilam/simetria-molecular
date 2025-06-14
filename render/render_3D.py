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

import pyvista as pv
import numpy as np
from render.render import Renderer
from model.model_molecula import Molecule
from model.model_grupo import Group

class MoleculeExplorer(Renderer):

    def __init__(self, metadata, molecule, group):
        self.metadata = metadata
        self.molecule = molecule
        self.group = group
        self.tamanho = {"C": 0.3, "H": 0.2}

    def render(self, resultados):
        """Summary
        """
        # Escolhe uma operação do grupo
        print(resultados)
        operacao_desejada = 1
        operacao = next((op for op in self.group.operacoes if op["id"] == operacao_desejada), None)
        destaque = self._converter_operacao_para_destaque(operacao)

        original = self.molecule
        transformada = self._aplicar_operacao(original, operacao)

        plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))

        # Exibe o nome da operação no rodapé
        plotter.add_text(f"Operação: {operacao['nome']}", position="lower_edge", font_size=12, color="black")

        # Antes
        plotter.subplot(0, 0)
        self._desenhar_molecula(plotter, original, "Antes da operação", destaque)

        # Depois
        plotter.subplot(0, 1)
        self._desenhar_molecula(plotter, transformada, "Depois da operação")

        plotter.link_views()
        plotter.show()

        return "Renderização local exibida"

    def _aplicar_operacao(self, molecule, operacao):
        """Summary
        """
        # Simula transformação: só inverte os eixos como exemplo
        print("\n=== MATRIZ DA OPERAÇÃO ===")
        print(operacao)
        novas_coords = [(-np.array(c)) for _, c in molecule.como_tuplas()]
        novos_elementos = [el for el, _ in molecule.como_tuplas()]
        return Molecule(nome="Transformada", elementos=novos_elementos, coordenadas=novas_coords)

    def _converter_operacao_para_destaque(self, operacao):
        destaques = []
        if "eixo" in operacao:
            destaques.append({
                "tipo": "eixo",
                "direcao": operacao["eixo"],
                "origem": [0, 0, 0]
            })
        if "plano_normal" in operacao:
            destaques.append({
                "tipo": "plano",
                "normal": operacao["plano_normal"],
                "origem": [0, 0, 0]
            })
        return destaques if destaques else None

    def _desenhar_molecula(self, plotter, molecula, titulo, destaques=None):
        cores = self._gerar_cores(len(molecula))
        self._desenhar_atomicos(plotter, molecula, cores)
        self._numerar_atomicos(plotter, molecula)
        self._desenhar_ligacoes(plotter, molecula)
        if destaques:
            self._destacar(plotter, destaques)
        plotter.add_text(titulo, font_size=12)

    def _gerar_cores(self, n):
        base = [
            (174, 198, 207), (255, 179, 71), (179, 158, 181),
            (119, 221, 119), (255, 105, 97), (253, 253, 150),
            (207, 207, 196), (244, 154, 194), (222, 165, 164),
            (176, 224, 230), (230, 230, 250), (197, 227, 132)
        ]
        return base[:n]

    def _desenhar_atomicos(self, plotter, molecula, cores):
        for i, (el, coord) in enumerate(molecula.como_tuplas()):
            raio = self.tamanho.get(el, 0.2)
            esfera = pv.Sphere(radius=raio, center=coord)
            plotter.add_mesh(esfera, color=cores[i % len(cores)], smooth_shading=True)

    def _numerar_atomicos(self, plotter, molecula):
        """Summary
        """
        print("Nao deveria >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for idx, (_, coord) in enumerate(molecula.como_tuplas(), start=1):
            plotter.add_point_labels([coord], [str(idx)], font_size=14, text_color='white', point_size=0, shape_opacity=0, always_visible=True)

    def _desenhar_ligacoes(self, plotter, molecula):
        coords = molecula.como_tuplas()
        for i, (_, c1) in enumerate(coords):
            for j, (_, c2) in enumerate(coords):
                if i < j:
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    if dist < 1.2:
                        plotter.add_mesh(pv.Line(c1, c2), color="gray", line_width=3)
        for i, (el1, c1) in enumerate(coords):
            for j, (el2, c2) in enumerate(coords):
                if i < j and el1 == 'C' and el2 == 'C':
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    if dist < 1.6:
                        plotter.add_mesh(pv.Line(c1, c2), color='black', line_width=4)

    def _destacar(self, plotter, destaques):
        """Summary
        """
        for d in destaques:
            tipo = d["tipo"]
            origem = np.array(d.get("origem", [0, 0, 0]))
            if tipo == "eixo":
                direcao = np.array(d["direcao"])
                direcao /= np.linalg.norm(direcao)
                linha = pv.Line(origem - 3.0 * direcao, origem + 3.0 * direcao, resolution=1)
                plotter.add_mesh(linha, color="gray", line_width=3)
            elif tipo == "plano":
                normal = np.array(d["normal"])
                plano = pv.Plane(center=origem, direction=normal / np.linalg.norm(normal), i_size=4.0, j_size=4.0)
                plotter.add_mesh(plano, color="gray", opacity=0.3, show_edges=False)