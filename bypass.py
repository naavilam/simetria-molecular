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

    def como_tuplas(self):
        return list(zip(self.elementos, self.coordenadas))


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
        return list(zip(self.molecula.elementos, coords.tolist()))

    def renderizar(self):
        transformada = self._transformar()
        plotter = pv.Plotter(shape=(1, 2), window_size=(1600, 800))
        plotter.subplot(0, 0)
        self._desenhar_molecula(self.molecula.como_tuplas(), plotter, "Antes da simetria")
        plotter.subplot(0, 1)
        self._desenhar_molecula(transformada, plotter, "Depois da simetria")
        plotter.link_views()
        plotter.show()

    def _desenhar_molecula(self, molecula, plotter, titulo):
        cores = self._gerar_cores(len(molecula))
        for i, (el, coord) in enumerate(molecula):
            cor = cores[i % len(cores)]
            raio = self.tamanho.get(el, 0.2)
            esfera = pv.Sphere(radius=raio, center=coord)
            plotter.add_mesh(esfera, color=cor, smooth_shading=True)
            plotter.add_point_labels([coord], [str(i+1)], font_size=14, text_color='white',
                                     point_size=0, shape_opacity=0, always_visible=True)

    def _gerar_cores(self, n):
        base = [
            (174, 198, 207), (255, 179, 71), (179, 158, 181),
            (119, 221, 119), (255, 105, 97), (253, 253, 150),
            (207, 207, 196), (244, 154, 194), (222, 165, 164),
            (176, 224, 230), (230, 230, 250), (197, 227, 132)
        ]
        return base[:n]



def main():
    grupo_path = "static/grupos/moleculares/D3d.json"
    molecula_path = "static/moleculas/etano_estrelado.xyz"
    operacao_id = "1"  # Altere para a operação desejada

    visualizador = OperacaoPyVistaRenderer(grupo_path, molecula_path, operacao_id)
    visualizador.renderizar()


if __name__ == "__main__":
    main()