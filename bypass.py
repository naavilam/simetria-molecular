import pyvista as pv
import numpy as np
import json

class Molecula:
    def __init__(self, caminho_arquivo):
        self.elementos, self.coordenadas = self._ler_xyz(caminho_arquivo)

    def _ler_xyz(self, path):
        with open(path, 'r') as f:
            linhas = f.readlines()
        natomos = int(linhas[0])
        elementos = []
        coordenadas = []
        for linha in linhas[2:2+natomos]:
            partes = linha.split()
            elementos.append(partes[0])
            coordenadas.append(list(map(float, partes[1:4])))
        return elementos, coordenadas


class OperacaoPyVistaRenderer:
    def __init__(self, caminho_grupo, caminho_molecula, id_operacao):
        self.grupo = self._carregar_grupo(caminho_grupo)
        self.molecula = Molecula(caminho_molecula)
        self.id_operacao = int(id_operacao)
        self.operacao = self._buscar_operacao()
        self.tamanho = {"C": 0.3, "H": 0.2}

    def _carregar_grupo(self, caminho):
        with open(caminho, 'r') as f:
            return json.load(f)

    def _buscar_operacao(self):
        for op in self.grupo["operacoes"]:
            print(op)
            if op.get("id") == self.id_operacao:
                return op
        raise ValueError(f"Operação com id '{self.id_operacao}' não encontrada.")

    def _gerar_matriz_rotacao(self, eixo, angulo_graus):
        ang = np.radians(angulo_graus)
        x, y, z = eixo / np.linalg.norm(eixo)
        c, s = np.cos(ang), np.sin(ang)
        return np.array([
            [c + x*x*(1-c),   x*y*(1-c) - z*s, x*z*(1-c) + y*s],
            [y*x*(1-c) + z*s, c + y*y*(1-c),   y*z*(1-c) - x*s],
            [z*x*(1-c) - y*s, z*y*(1-c) + x*s, c + z*z*(1-c)]
        ])

    def _transformar(self):
        tipo = self.operacao["tipo"]
        coords = np.array(self.molecula.coordenadas)
        if tipo in ["rotacao", "impropria"]:
            eixo = np.array(self.operacao["eixo"])
            angulo = self.operacao["angulo"]
            R = self._gerar_matriz_rotacao(eixo, angulo)
            coords = coords @ R.T
            if tipo == "impropria":
                plano = np.array(self.operacao["plano_normal"])
                plano = plano / np.linalg.norm(plano)
                coords = coords - 2 * np.outer(np.dot(coords, plano), plano)
        elif tipo == "reflexao":
            plano = np.array(self.operacao["plano_normal"])
            plano = plano / np.linalg.norm(plano)
            coords = coords - 2 * np.outer(np.dot(coords, plano), plano)
        elif tipo == "inversao":
            coords = -coords
        return list(zip(self.molecula.elementos, coords.tolist()))

    def renderizar(self):
        transformada = self._transformar()
        plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
        plotter.subplot(0, 0)
        destaques = self._gerar_destaques_da_operacao(self.operacao)
        self._desenhar_molecula(list(zip(self.molecula.elementos, self.molecula.coordenadas)), plotter, "Antes da simetria", destaques)
        plotter.subplot(0, 1)
        self._desenhar_molecula(transformada, plotter, "Depois da simetria")
        plotter.link_views()
        plotter.show()

    def _desenhar_ligacoes(self, molecula, plotter):
        coords = molecula
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

    def _desenhar_molecula(self, molecula, plotter, titulo, destaque=None):
        cores = self._gerar_cores(len(molecula))

        # Identificar carbonos
        carbonos = [(i, coord) for i, (el, coord) in enumerate(molecula) if el == "C"]
        c1_idx = min(carbonos, key=lambda x: x[1][2])[0]  # menor z
        c2_idx = max(carbonos, key=lambda x: x[1][2])[0]  # maior z
        c1_coord = molecula[c1_idx][1]
        c2_coord = molecula[c2_idx][1]

        # Inicializar dicionário de rótulos
        rotulos = {c1_idx: 1, c2_idx: 2}
        h_proximos_c1 = []
        h_proximos_c2 = []

        for i, (el, coord) in enumerate(molecula):
            if i in (c1_idx, c2_idx):
                continue
            dist_c1 = np.linalg.norm(np.array(coord) - np.array(c1_coord))
            dist_c2 = np.linalg.norm(np.array(coord) - np.array(c2_coord))
            if dist_c1 < dist_c2:
                h_proximos_c1.append((i, dist_c1))
            else:
                h_proximos_c2.append((i, dist_c2))

        # Ordenar para manter consistência visual
        h_proximos_c1.sort(key=lambda x: x[1])
        h_proximos_c2.sort(key=lambda x: x[1])

        for offset, (i, _) in enumerate(h_proximos_c1):
            rotulos[i] = 3 + offset
        for offset, (i, _) in enumerate(h_proximos_c2):
            rotulos[i] = 6 + offset

        # Desenhar átomos e rótulos
        for i, (el, coord) in enumerate(molecula):
            cor = cores[i % len(cores)]
            raio = self.tamanho.get(el, 0.2)
            esfera = pv.Sphere(radius=raio, center=coord)
            plotter.add_mesh(esfera, color=cor, smooth_shading=True)
            plotter.add_point_labels([coord], [str(rotulos[i])], font_size=14, text_color='white',
                                     point_size=0, shape_opacity=0, always_visible=True)

        self._desenhar_ligacoes(molecula, plotter)
        if destaque:
            self._destacar(destaque, plotter)

    def _destacar(self, destaque, plotter):
        print(destaque)
        destaques = destaque if isinstance(destaque, list) else [destaque]
        for d in destaques:
            tipo = d["tipo"]
            centro = np.array(d.get("origem", [0.0, 0.0, 0.0]))

            if tipo == "eixo":
                mesh = self._gerar_eixo(d, centro)
                plotter.add_mesh(mesh, color="gray", line_width=3)

            elif tipo == "plano":
                mesh = self._gerar_plano(d, centro)
                plotter.add_mesh(mesh, color="gray", opacity=0.3, show_edges=False)

            elif tipo == "ponto":
                mesh = self._gerar_ponto(centro)
                plotter.add_mesh(mesh, color="gray", opacity=0.5)

            else:
                print(f"[AVISO] Tipo de destaque desconhecido: {tipo}")

    def _gerar_cores(self, n):
        base = [
            (174, 198, 207), (255, 179, 71), (179, 158, 181),
            (119, 221, 119), (255, 105, 97), (253, 253, 150),
            (207, 207, 196), (244, 154, 194), (222, 165, 164),
            (176, 224, 230), (230, 230, 250), (197, 227, 132)
        ]
        return base[:n]

    def _gerar_eixo(self, d, centro):
        vetor = np.array(d["direcao"], dtype=float)
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

    def _gerar_destaques_da_operacao(self, op):
        destaques = []

        # Eixo (rotacao ou impropria)
        # if "eixo" in op and isinstance(op["eixo"], list):
        #     destaques.append({
        #         "tipo": "eixo",
        #         "direcao": op["eixo"],
        #         "origem": op.get("origem", [0.0, 0.0, 0.0])
        #     })

        # Plano (reflexao ou impropria)
        if "plano_normal" in op and isinstance(op["plano_normal"], list):
            destaques.append({
                "tipo": "plano",
                "normal": op["plano_normal"],
                "origem": op.get("origem", [0.0, 0.0, 0.0])
            })

        if op["tipo"] == "inversao":
            destaques.append({
                "tipo": "ponto",
                "origem": [0, 0, 0]
            })
        # # Ponto (se não houver nem eixo nem plano, mas houver origem)
        # if "origem" in op and "eixo" not in op and "plano_normal" not in op:
        #     destaques.append({
        #         "tipo": "ponto",
        #         "origem": op["origem"]
        #     })

        return destaques

def main():
    grupo_path = "static/grupos/moleculares/D3d.json"
    molecula_path = "static/moleculas/etano_estrelado.xyz"


    for operacao_id in range(11, 12):
        print(f"\n>>> Renderizando operação {operacao_id}...\n")
        visualizador = OperacaoPyVistaRenderer(grupo_path, molecula_path, operacao_id)
        visualizador.renderizar()
        input("Pressione Enter para continuar para a próxima operação...")


if __name__ == "__main__":
    main()