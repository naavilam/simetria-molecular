# import pyvista as pv
# import numpy as np

# def visualizar_pyvista(original, transformada, titulo="Simetria aplicada", destaque=None):
#     plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
#     tamanho = {"C": 0.3, "H": 0.2}

#     def desenhar_molecula(molecula, title, destaque=None):
#         plotter.add_text(title, font_size=12)
#         cores = pv.Color.hexcolors[:len(molecula)]

#         for i, (el, coord) in enumerate(molecula):
#             cor = cores[i % len(cores)]
#             raio = tamanho.get(el, 0.2)
#             esfera = pv.Sphere(radius=raio, center=coord)
#             plotter.add_mesh(esfera, color=cor, smooth_shading=True)
#             plotter.add_point_labels([coord], [str(i+1)], font_size=12, point_color='black', text_color='black')

#         for i, (_, c1) in enumerate(molecula):
#             for j, (_, c2) in enumerate(molecula):
#                 if i < j:
#                     dist = np.linalg.norm(np.array(c1) - np.array(c2))
#                     if dist < 1.2:
#                         linha = pv.Line(c1, c2)
#                         plotter.add_mesh(linha, color="gray", line_width=3)

#         if destaque:
#             tipo, vetor = destaque
#             centro = np.array([0.0, 0.0, 0.0])
#             if tipo == "eixo":
#                 seta = pv.Arrow(start=centro - vetor, direction=2 * vetor, tip_length=0.2)
#                 plotter.add_mesh(seta, color="blue", opacity=0.6)
#             elif tipo == "plano":
#                 normal = vetor / np.linalg.norm(vetor)
#                 v = np.cross(normal, [1, 0, 0])
#                 if np.allclose(v, 0):
#                     v = np.cross(normal, [0, 1, 0])
#                 v /= np.linalg.norm(v)
#                 w = np.cross(normal, v)
#                 lado = 2.0
#                 pontos = [
#                     centro + lado * (v + w),
#                     centro + lado * (v - w),
#                     centro + lado * (-v - w),
#                     centro + lado * (-v + w),
#                 ]
#                 face = pv.Polygon(pontos)
#                 plotter.add_mesh(face, color="cyan", opacity=0.3)

#     # Molecula original
#     plotter.subplot(0, 0)
#     desenhar_molecula(original, "Antes da simetria", destaque=destaque)

#     # Molecula transformada
#     plotter.subplot(0, 1)
#     desenhar_molecula(transformada, "Depois da simetria", destaque=None)

#     plotter.add_text(titulo, position="upper_edge", font_size=14, color="black")
#     plotter.show()



# import pyvista as pv
# import numpy as np


# import pyvista as pv
# import numpy as np

# def visualizar_pyvista(original, transformada, titulo="Simetria aplicada", destaque=None):
#     plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
#     tamanho = {"C": 0.3, "H": 0.2}

#     def desenhar_molecula(molecula, title, destaque=None):
#         plotter.add_text(title, font_size=12)
#         cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)][:len(molecula)]

#         for i, (el, coord) in enumerate(molecula):
#             cor = cores[i % len(cores)]
#             raio = tamanho.get(el, 0.2)
#             esfera = pv.Sphere(radius=raio, center=coord)
#             plotter.add_mesh(esfera, color=cor, smooth_shading=True)
#             plotter.add_point_labels([coord], [str(i+1)], font_size=12, point_color='black', text_color='black')

#         for i, (_, c1) in enumerate(molecula):
#             for j, (_, c2) in enumerate(molecula):
#                 if i < j:
#                     dist = np.linalg.norm(np.array(c1) - np.array(c2))
#                     if dist < 1.2:
#                         linha = pv.Line(c1, c2)
#                         plotter.add_mesh(linha, color="gray", line_width=3)

#         if destaque:
#             tipo, vetor = destaque
#             centro = np.array([0.0, 0.0, 0.0])
#             if tipo == "eixo":
#                 seta = pv.Arrow(start=centro - vetor, direction=2 * vetor, tip_length=0.2)
#                 plotter.add_mesh(seta, color="blue", opacity=0.6)
#             elif tipo == "plano":
#                 normal = vetor / np.linalg.norm(vetor)
#                 v = np.cross(normal, [1, 0, 0])
#                 if np.allclose(v, 0):
#                     v = np.cross(normal, [0, 1, 0])
#                 v /= np.linalg.norm(v)
#                 w = np.cross(normal, v)
#                 lado = 2.0
#                 pontos = [
#                     centro + lado * (v + w),
#                     centro + lado * (v - w),
#                     centro + lado * (-v - w),
#                     centro + lado * (-v + w),
#                 ]
#                 face = pv.Polygon(pontos)
#                 plotter.add_mesh(face, color="cyan", opacity=0.3)

#     # Molecula original
#     plotter.subplot(0, 0)
#     desenhar_molecula(original, "Antes da simetria", destaque=destaque)

#     # Molecula transformada
#     plotter.subplot(0, 1)
#     desenhar_molecula(transformada, "Depois da simetria", destaque=None)

#     plotter.add_text(titulo, position="upper_edge", font_size=14, color="black")
#     plotter.show()


# import pyvista as pv
# import numpy as np

# def visualizar_pyvista(original, transformada, titulo="Simetria aplicada", destaque=None):
#     plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
#     tamanho = {"C": 0.3, "H": 0.2}

#     def desenhar_molecula(molecula, title, destaque=None):
#         plotter.add_text(title, font_size=12)
#         cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)][:len(molecula)]

#         for i, (el, coord) in enumerate(molecula):
#             cor = cores[i % len(cores)]
#             raio = tamanho.get(el, 0.2)
#             esfera = pv.Sphere(radius=raio, center=coord)
#             plotter.add_mesh(esfera, color=cor, smooth_shading=True)

#         # Numeração dos átomos
#         for idx, (elem, coord) in enumerate(molecula):
#             plotter.add_point_labels([coord], [str(idx+1)],
#                                      font_size=14, text_color='black', always_visible=True)
#         # Ligação explícita entre átomos 1 e 2
#         if len(molecula) >= 2:
#             p1 = np.array(molecula[0][1])
#             p2 = np.array(molecula[1][1])
#             plotter.add_lines(np.array([p1, p2]), color="black", width=6)

#         for i, (_, c1) in enumerate(molecula):
#             for j, (_, c2) in enumerate(molecula):
#                 if i < j:
#                     dist = np.linalg.norm(np.array(c1) - np.array(c2))
#                     if dist < 1.2:
#                         linha = pv.Line(c1, c2)
#                         plotter.add_mesh(linha, color="gray", line_width=3)

#         if destaque:
#             tipo, vetor = destaque
#             centro = np.array([0.0, 0.0, 0.0])
#             if tipo == "eixo":
#                 seta = pv.Arrow(start=centro - vetor, direction=2 * vetor, tip_length=0.2)
#                 plotter.add_mesh(seta, color="blue", opacity=0.6)
#             elif tipo == "plano":
#                 normal = vetor / np.linalg.norm(vetor)
#                 v = np.cross(normal, [1, 0, 0])
#                 if np.allclose(v, 0):
#                     v = np.cross(normal, [0, 1, 0])
#                 v /= np.linalg.norm(v)
#                 w = np.cross(normal, v)
#                 lado = 2.0
#                 pontos = [
#                     centro + lado * (v + w),
#                     centro + lado * (v - w),
#                     centro + lado * (-v - w),
#                     centro + lado * (-v + w),
#                 ]
#                 face = pv.Polygon(pontos)
#                 plotter.add_mesh(face, color="cyan", opacity=0.3)

#     # Molecula original
#     plotter.subplot(0, 0)
#     desenhar_molecula(original, "Antes da simetria", destaque=destaque)

#     # Molecula transformada
#     plotter.subplot(0, 1)
#     desenhar_molecula(transformada, "Depois da simetria", destaque=None)

#     plotter.add_text(titulo, position="upper_edge", font_size=14, color="black")
#     plotter.show()


# import pyvista as pv
# import numpy as np

# def visualizar_pyvista(original, transformada, titulo="Simetria aplicada", destaque=None):
#     plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
#     tamanho = {"C": 0.3, "H": 0.2}

#     def desenhar_molecula(molecula, title, destaque=None):
#         plotter.add_text(title, font_size=12)
#         cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)][:len(molecula)]

#         for i, (el, coord) in enumerate(molecula):
#             cor = cores[i % len(cores)]
#             raio = tamanho.get(el, 0.2)
#             esfera = pv.Sphere(radius=raio, center=coord)
#             plotter.add_mesh(esfera, color=cor, smooth_shading=True)

#         # Numeração dos átomos
#         for idx, (elem, coord) in enumerate(molecula):
#             plotter.add_point_labels([coord], [str(idx+1)],
#                                      font_size=14, text_color='black', always_visible=True)
#         # Ligação explícita entre átomos 1 e 2
#         if len(molecula) >= 2:
#             p1 = np.array(molecula[0][1])
#             p2 = np.array(molecula[1][1])
#             plotter.add_lines(np.array([p1, p2]), color="black", width=6)

#         for i, (_, c1) in enumerate(molecula):
#             for j, (_, c2) in enumerate(molecula):
#                 if i < j:
#                     dist = np.linalg.norm(np.array(c1) - np.array(c2))
#                     if dist < 1.2:
#                         linha = pv.Line(c1, c2)
#                         plotter.add_mesh(linha, color="gray", line_width=3)

#         if destaque:
#                 # suporte a múltiplos destaques (eixo/plano)
#             destaques = destaque if isinstance(destaque, list) else [destaque]
#             for tipo, vetor in destaques:
#                 centro = np.array([0.0, 0.0, 0.0])
#                 if tipo == "eixo":
#                     seta = pv.Arrow(start=centro - vetor, direction=2 * vetor, tip_length=0.2)
#                     plotter.add_mesh(seta, color="blue", opacity=0.6)
#                 elif tipo == "plano":
#                     normal = vetor / np.linalg.norm(vetor)
#                     v = np.cross(normal, [1, 0, 0])
#                     if np.linalg.norm(v) < 1e-3:
#                         v = np.cross(normal, [0, 1, 0])
#                     v = v / np.linalg.norm(v)
#                     w = np.cross(normal, v)
#                     lado = 2.0
#                     v *= lado
#                     w *= lado
#                     pontos = [
#                         centro + v + w,
#                         centro + v - w,
#                         centro - v - w,
#                         centro - v + w
#                     ]
#                     face = pv.Polygon(pontos)
#                     plotter.add_mesh(face, color="cyan", opacity=0.3)
#             centro = np.array([0.0, 0.0, 0.0])
#             if tipo == "eixo":
#                 seta = pv.Arrow(start=centro - vetor, direction=2 * vetor, tip_length=0.2)
#                 plotter.add_mesh(seta, color="blue", opacity=0.6)
#             elif tipo == "plano":
#                 normal = vetor / np.linalg.norm(vetor)
#                 v = np.cross(normal, [1, 0, 0])
#                 if np.allclose(v, 0):
#                     v = np.cross(normal, [0, 1, 0])
#                 v /= np.linalg.norm(v)
#                 w = np.cross(normal, v)
#                 lado = 2.0
#                 pontos = [
#                     centro + lado * (v + w),
#                     centro + lado * (v - w),
#                     centro + lado * (-v - w),
#                     centro + lado * (-v + w),
#                 ]
#                 face = pv.Polygon(pontos)
#                 plotter.add_mesh(face, color="cyan", opacity=0.3)

#     # Molecula original
#     plotter.subplot(0, 0)
#     desenhar_molecula(original, "Antes da simetria", destaque=destaque)

#     # Molecula transformada
#     plotter.subplot(0, 1)
#     desenhar_molecula(transformada, "Depois da simetria", destaque=None)

#     plotter.add_text(titulo, position="upper_edge", font_size=14, color="black")
#     plotter.show()
