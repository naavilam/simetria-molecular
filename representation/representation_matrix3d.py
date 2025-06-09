import numpy as np
from representation.representation import Representation

class Matrix3DRepresentation(Representation):
    def __init__(self, nome_grupo: str):
        super().__init__(nome_grupo)
        self._dados = {}  # nome da operação → matriz 3x3

    def __iter__(self):
        return iter(self._dados.items())

    @classmethod
    def from_group(cls, grupo):
        inst = cls(grupo.nome)
        for op in grupo.operacoes:
            matriz = cls._matriz_da_operacao(op)
            inst.adicionar(op["nome"], matriz)
        return inst  # <<<<<< GARANTA que isso existe!

    @staticmethod
    def _matriz_da_operacao(op):
        if op["tipo"] == "identidade":
            return np.identity(3)

        elif op["tipo"] == "rotacao":
            eixo = np.array(op["eixo"])
            angulo = np.deg2rad(op["angulo"])
            return Matrix3DRepresentation._matriz_rotacao(eixo, angulo)

        elif op["tipo"] == "reflexao":
            normal = np.array(op["plano_normal"])
            return Matrix3DRepresentation._matriz_reflexao(normal)

        elif op["tipo"] == "inversao":
            return -np.identity(3)

        elif op["tipo"] == "impropria":
            eixo = np.array(op["eixo"])
            angulo = np.deg2rad(op["angulo"])
            rot = Matrix3DRepresentation._matriz_rotacao(eixo, angulo)
            plano = np.array(op["plano_normal"])
            refl = Matrix3DRepresentation._matriz_reflexao(plano)
            return refl @ rot

        else:
            raise ValueError(f"Tipo de operação desconhecido: {op['tipo']}")

    @staticmethod
    def _matriz_rotacao(eixo, angulo):
        eixo = eixo / np.linalg.norm(eixo)
        x, y, z = eixo
        c = np.cos(angulo)
        s = np.sin(angulo)
        C = 1 - c
        return np.array([
            [x*x*C + c,   x*y*C - z*s, x*z*C + y*s],
            [y*x*C + z*s, y*y*C + c,   y*z*C - x*s],
            [z*x*C - y*s, z*y*C + x*s, z*z*C + c  ]
        ])

    @staticmethod
    def _matriz_reflexao(normal):
        n = normal / np.linalg.norm(normal)
        return np.identity(3) - 2 * np.outer(n, n)

    def adicionar(self, nome, dados):
        self._dados[nome] = dados

    def aplicar(self, nome, vetor):
        matriz = self._dados[nome]
        return np.dot(matriz, vetor)

    def compor(self, a, b):
        return a @ b

    def inverso(self, a):
        return np.linalg.inv(a)

    def conjugar(self, a, b):
        return self.inverso(b) @ a @ b

    def nomes(self):
        return list(self._dados.keys())

    def valores(self):
        return list(self._dados.values())

    def __getitem__(self, nome):
        return self._dados[nome]