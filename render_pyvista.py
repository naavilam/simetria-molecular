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

def visualizar_pyvista(
    original,
    transformada,
    titulo="Simetria aplicada",
    destaque=None):
    """Summary
    """
    plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
    tamanho = {"C": 0.3, "H": 0.2}

    def desenhar_molecula(molecula, title, destaque=None):
        """Summary
        """
        plotter.add_text(title, font_size=12)
        # cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255,
        #                                                                 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)][:len(molecula)]

        cores = [
        (174, 198, 207),   # azul pastel
        (255, 179, 71),    # laranja claro
        (179, 158, 181),   # lavanda
        (119, 221, 119),   # verde claro
        (255, 105, 97),    # vermelho suave
        (253, 253, 150),   # amarelo manteiga
        (207, 207, 196),   # cinza leve
        (244, 154, 194),   # rosa bebê
        (222, 165, 164),   # rosado neutro
        (176, 224, 230),   # azul piscina
        (230, 230, 250),   # lavanda clarinha
        (197, 227, 132),   # verde amarelado
        ][:len(molecula)]

        # Adiciona cores:
        for i, (el, coord) in enumerate(molecula.como_tuplas()):
            cor = cores[i % len(cores)]
            raio = tamanho.get(el, 0.2)
            esfera = pv.Sphere(radius=raio, center=coord)
            plotter.add_mesh(esfera, color=cor, smooth_shading=True)

        # Numeração dos átomos:
        # for idx, (elem, coord) in enumerate(molecula):
        #     plotter.add_point_labels([coord], [str(idx + 1)],
        #                              font_size=14, text_color='white', point_size=0, shape_opacity=0, always_visible=True)
        
        # Numera só os vizinhos, pulando o índice 0 (átomo central)
        counter = 1
        for idx, (elem, coord) in enumerate(molecula.como_tuplas()):
            if idx == 0:
                continue   # pula o átomo do meio
            plotter.add_point_labels(
                [coord], [str(counter)],
                font_size=14,
                text_color='white',
                point_size=0,
                shape_opacity=0,
                always_visible=True
            )
            counter += 1
    
        # todas as ligações
        # for i, (el1, c1) in enumerate(molecula):
        #     for j, (el2, c2) in enumerate(molecula):
        #         if i < j:
        #             dist = np.linalg.norm(np.array(c1) - np.array(c2))
        #             # C–H
        #             if {el1, el2} == {'C','H'} and dist < 1.2:
        #                 cor = 'gray'; lw = 3
        #             # C–C
        #             elif el1 == 'C' and el2 == 'C' and dist < 1.6:
        #                 cor = 'black'; lw = 4
        #             else:
        #                 continue
        #             linha = pv.Line(c1, c2)
        #             plotter.add_mesh(linha, color=cor, line_width=lw)


        # 1. Ligações simples (ex: C–H)
        for i, (_, c1) in enumerate(molecula.como_tuplas()):
            for j, (_, c2) in enumerate(molecula.como_tuplas()):
                if i < j:
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    if dist < 1.2:
                        linha = pv.Line(c1, c2)
                        plotter.add_mesh(linha, color="gray", line_width=3)

        # 1. Ligações simples (ex: C–C)
        for i, (el1, c1) in enumerate(molecula.como_tuplas()):
            for j, (el2, c2) in enumerate(molecula.como_tuplas()):
                if i < j and el1 == 'C' and el2 == 'C':
                    dist = np.linalg.norm(np.array(c1) - np.array(c2))
                    # corte típico para C–C simples ~1.5 Å
                    if dist < 1.6:
                        linha = pv.Line(c1, c2)
                        plotter.add_mesh(linha, color='black', line_width=4)

        # 2. Ligações do anel com alternância
        # anel = [0, 1, 2, 3, 4, 5]
        # pares_anel = [(anel[i], anel[(i+1)%6]) for i in range(6)]

        # for k, (i, j) in enumerate(pares_anel):
        #     c1 = molecula[i][1]
        #     c2 = molecula[j][1]
        #     if k % 2 == 0:
        #         deslocamento = 0.05 * np.cross(np.array(c2)-np.array(c1), [0,0,1])
        #         norm = np.linalg.norm(deslocamento)
        #         deslocamento = deslocamento / norm * 0.05 if norm != 0 else np.array([0.05,0,0])
        #         l1 = pv.Line(np.array(c1)+deslocamento, np.array(c2)+deslocamento)
        #         l2 = pv.Line(np.array(c1)-deslocamento, np.array(c2)-deslocamento)
        #         plotter.add_mesh(l1, color="black", line_width=4)
        #         plotter.add_mesh(l2, color="black", line_width=4)
        #     else:
        #         l = pv.Line(c1, c2)
        #         plotter.add_mesh(l, color="black", line_width=4)

        if destaque:
            destaques = destaque if isinstance(destaque, list) else [destaque]
            for d in destaques:
                tipo = d["tipo"]
                centro = np.array(d.get("origem", [0.0, 0.0, 0.0]))

                if tipo == "eixo":
                    vetor = np.array(d["direcao"])
                    vetor = vetor / np.linalg.norm(vetor)
                    comprimento = 3.0
                    linha = pv.Line(
                        pointa=centro - comprimento * vetor,
                        pointb=centro + comprimento * vetor,
                        resolution=1
                    )
                    plotter.add_mesh(linha, color="gray", line_width=3, style="surface")

                    # nome = d.get("nome", "")
                    # print(nome)
                    # label = pv.Text3D(nome, depth=0.1)
                    # label.translate(centro + deslocamento)
                    # plotter.add_mesh(label, color="black")
                    # plotter.add_point_labels(
                    #     [centro],
                    #     [nome],
                    #     font_size=14,
                    #     text_color="black",
                    #     point_size=0,
                    #     shape_opacity=0,
                    #     always_visible=True
                    # )




                elif tipo == "plano":
                    normal = np.array(d["normal"])
                    plano = pv.Plane(
                        center=centro,
                        direction=normal / np.linalg.norm(normal),
                        i_size=4.0,
                        j_size=4.0
                    )
                    plotter.add_mesh(plano, color="gray", opacity=0.3, show_edges=False)
                    # nome = d.get("nome", "")
                    # print(nome)
                    # label = pv.Text3D(nome, depth=0.1)
                    # label.translate(centro + deslocamento)
                    # plotter.add_mesh(label, color="black")
                    # plotter.add_point_labels(
                    #     [centro],
                    #     [nome],
                    #     font_size=14,
                    #     text_color="black",
                    #     point_size=0,
                    #     shape_opacity=0,
                    #     always_visible=True
                    # )

                elif tipo == "ponto":
                    esfera = pv.Sphere(radius=0.1, center=centro)
                    plotter.add_mesh(esfera, color="gray", opacity=0.5)
                    # nome = d.get("nome", "")
                    # print(nome)
                    # label = pv.Text3D(nome, depth=0.1)
                    # label.translate(centro + deslocamento)
                    # plotter.add_mesh(label, color="black")

                    # plotter.add_point_labels(
                    #     [centro],
                    #     [nome],
                    #     font_size=14,
                    #     text_color="black",
                    #     point_size=0,
                    #     shape_opacity=0,
                    #     always_visible=True
                    # )

                else:
                    print(f"[AVISO] Tipo de destaque desconhecido: {tipo}")

        # if destaque.any():
        #     # suporte a múltiplos destaques (eixo/plano)
        #     destaques = destaque if isinstance(destaque, list) else [destaque]
        #     for tipo, vetor in destaques:
        #         centro = np.array([0.0, 0.0, 0.0])
        #         if tipo == "eixo":
        #             seta = pv.Arrow(
        #                 start=centro - vetor,
        #                 direction=2 * vetor,
        #                 tip_length=0.2)
        #             plotter.add_mesh(seta, color="blue", opacity=0.6)
        #         elif tipo == "plano":
        #               # Plano de reflexão: use pv.Plane para evitar erros de
        #               # SetCenter
        #             normal = vetor / np.linalg.norm(vetor)
        #             centro = np.array([0.0, 0.0, 0.0])
        #             plano = pv.Plane(
        #                 center=centro,
        #                 direction=normal,
        #                 i_size=4.0,   # largura do plano
        #                 j_size=4.0    # altura do plano
        #             )
        #             plotter.add_mesh(plano, color="cyan", opacity=0.3, show_edges=False)
        #             centro = np.array([0.0, 0.0, 0.0])
        #             if tipo == "eixo":
        #                 seta = pv.Arrow(start=centro - vetor, direction=2 * vetor, tip_length=0.2)
        #                 plotter.add_mesh(seta, color="blue", opacity=0.6)
        #             elif tipo == "plano":
        #                 # Plano de reflexão: use pv.Plane para evitar erros
        #                 # de SetCenter
        #                 normal = vetor / np.linalg.norm(vetor)
        #                 centro = np.array([0.0, 0.0, 0.0])
        #                 plano = pv.Plane(
        #                     center=centro,
        #                     direction=normal,
        #                     i_size=4.0,   # largura do plano
        #                     j_size=4.0    # altura do plano
        #                 )
        #                 plotter.add_mesh(
        #                     plano, color="cyan", opacity=0.3, show_edges=False)
    # Molecula original
    plotter.subplot(0, 0)
    desenhar_molecula(original, "Antes da simetria", destaque=destaque)
    # Molecula transformada
    plotter.subplot(0, 1)
    desenhar_molecula(transformada, "Depois da simetria", destaque=None)
    # Ajuste fino da câmera
    # parâmetros: (pos_camera), (foco_no_ponto), (vetor_up)
    # new_cam_pos = [(3, -3, 2),  # x, y, z da câmera
    #                (0, 0, 0),   # ponto focal (centro da molécula)
    #                (0, 0, 1)]   # “para onde é cima” (eixo Z)

    # plotter.camera_position = new_cam_pos


    plotter.add_text(
        titulo,
        position="upper_edge",
        font_size=14,
        color="black")
    # Linka as câmeras de todas as views:
    plotter.link_views()

    # Agora qualquer alteração na camera.afetará ambos:
    plotter.camera.azimuth -= 25 # gira
    plotter.camera.elevation -= 20  # ergue a câmera
    plotter.camera.roll +=  1     # inclina a cena no plano da tela
    plotter.show()
