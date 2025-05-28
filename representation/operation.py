"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-05-26                                                                **
**                                                      License: Custom Attribution License                                                       **
**                                                                                                                                                **
**                                                                      ---                                                                       **
**                                                                                                                                                **
**   Permission is granted to use, copy, modify, and distribute this file, provided that this notice is retained in full and that the origin of   **
**    the software is clearly and explicitly attributed to the original author. Such attribution must be preserved not only within the source     **
**       code, but also in any accompanying documentation, public display, distribution, or derived work, in both digital or printed form.        **
**                                                  For licensing inquiries: contact@chanah.dev                                                   **
====================================================================================================================================================
"""

import numpy as np
from scipy.spatial.transform import Rotation as R
from core.molecule import Molecule

class Operation:
    """Representa uma única operação de simetria e gera a matriz associada."""
    
    def __init__(self, tipo, id=None, nome=None, eixo=None, angulo=None, plano_normal=None, origem=None, comentario=None):
        self.tipo = tipo
        self.nome = nome
        self.eixo = eixo
        self.angulo = angulo
        self.plano_normal = plano_normal
        self.origem = origem or [0.0, 0.0, 0.0]
        self.comentario = comentario
        self.id = id

    @classmethod
    def from_dict(cls, d):
        return cls(
            tipo=d.get("tipo"),
            id = d.get("id"),
            nome=d.get("nome"),
            eixo=d.get("eixo"),
            angulo=d.get("angulo"),
            plano_normal=d.get("plano_normal"),
            origem=d.get("origem", [0.0, 0.0, 0.0]),
            comentario=d.get("comentario")
        )

    def execute(self, molecule):
        Rmat = self._matriz()
        elementos = [el for el, _ in molecule.como_tuplas()]
        coords = [Rmat @ np.array(coord) for _, coord in molecule.como_tuplas()]
        nova = Molecule.__new__(Molecule)
        nova.elementos = elementos
        nova.coordenadas = coords
        return nova

    def _matriz(self):
        """Retorna a matriz de transformação associada à operação."""
        if self.tipo == "identidade":
            return np.eye(3)

        elif self.tipo == "rotacao":
            eixo = np.array(self.eixo, dtype=float)
            eixo /= np.linalg.norm(eixo)
            rot = R.from_rotvec(np.deg2rad(self.angulo) * eixo)
            return rot.as_matrix()

        elif self.tipo == "reflexao":
            n = np.array(self.plano_normal, dtype=float)
            n /= np.linalg.norm(n)
            return np.eye(3) - 2 * np.outer(n, n)

        elif self.tipo == "impropria":
            eixo = np.array(self.eixo, dtype=float)
            eixo /= np.linalg.norm(eixo)
            rot = R.from_rotvec(np.deg2rad(self.angulo) * eixo).as_matrix()
            n = np.array(self.plano_normal, dtype=float)
            n /= np.linalg.norm(n)
            reflexao = np.eye(3) - 2 * np.outer(n, n)
            return reflexao @ rot

        elif self.tipo == "inversao":
            return -np.eye(3)

        else:
            raise ValueError(f"Tipo de operação desconhecido: {self.tipo}")

    def destaque(self):
        """Retorna estrutura que descreve eixo/plano/ponto de destaque visual."""
        if self.tipo == "identidade":
            return None

        elif self.tipo == "rotacao":
            return {
                "tipo": "eixo",
                "origem": self.origem,
                "direcao": np.array(self.eixo).tolist()
            }

        elif self.tipo == "reflexao":
            return {
                "tipo": "plano",
                "origem": self.origem,
                "normal": np.array(self.plano_normal).tolist()
            }

        elif self.tipo == "impropria":
            return [
                {
                    "tipo": "eixo",
                    "origem": self.origem,
                    "direcao": np.array(self.eixo).tolist()
                },
                {
                    "tipo": "plano",
                    "origem": self.origem,
                    "normal": np.array(self.plano_normal).tolist()
                }
            ]

        elif self.tipo == "inversao":
            return {
                "tipo": "ponto",
                "origem": self.origem
            }

        else:
            raise ValueError(f"Tipo de operação desconhecido: {self.tipo}")