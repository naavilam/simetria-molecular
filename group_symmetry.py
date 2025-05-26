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

import numpy as np
from scipy.spatial.transform import Rotation as R
import json

class GroupSymmetry:

    """Summary
    """
    def __init__(self, dados):
        """Summary
        """
        self.dados = dados

    @classmethod
    def from_file(cls, path_json):
        path = path_json
        dados = cls._carregar(path_json)
        return cls(dados=dados)

    @classmethod
    def _carregar(cls, path_json):
        """Summary
        """
        with open(path_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_operacoes(self):
        """Summary
        """
        return self.dados.get("operacoes", [])

    @staticmethod
    def detalhe_operacao(operacao):
        """Retorna a operacao e o eixo/plano de simetria da operacao
        
        Args:
            operacao (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            ValueError: Description
        """
        tipo = operacao["tipo"]

        if tipo == "identidade":
            return np.eye(3), None

        elif tipo == "rotacao":
            eixo = np.array(operacao["eixo"])
            angulo = operacao["angulo"]
            eixo = eixo / np.linalg.norm(eixo)
            rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()

            destaque = {
                "tipo": "eixo",
                "origem": [0, 0, 0],
                "direcao": eixo.tolist(),
            }
            return rot, destaque

        elif tipo == "reflexao":
            n = np.array(operacao["plano_normal"])
            n = n / np.linalg.norm(n)
            reflexao = np.eye(3) - 2 * np.outer(n, n)

            destaque = {
                "tipo": "plano",
                "origem": [0, 0, 0],
                "normal": n.tolist(),
            }
            return reflexao, destaque

        elif tipo == "impropria":
            eixo = np.array(operacao["eixo"], float)
            angulo = operacao["angulo"]
            eixo /= np.linalg.norm(eixo)
            rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()

            normal = np.array(operacao["plano_normal"], float)
            normal /= np.linalg.norm(normal)
            plano = np.eye(3) - 2 * np.outer(normal, normal)

            destaque = [
                {
                    "tipo":   "eixo",
                    "origem": [0, 0, 0],
                    "direcao": eixo.tolist(),
                },
                {
                    "tipo":   "plano",
                    "origem": [0, 0, 0],
                    "normal": normal.tolist(),
                }
            ]
            return plano @ rot, destaque

        elif tipo == "inversao":
            centro = operacao.get("origem", [0, 0, 0])
            inversao = -np.eye(3)
            destaque = {
                "tipo": "ponto",
                "origem": centro,
            }
            return inversao, destaque

        else:
            raise ValueError(f"Tipo de operação desconhecido: {tipo}")
