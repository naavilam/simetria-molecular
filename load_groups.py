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

class GrupoSimetria:

    """Summary
    """
    
    def __init__(self, path_arquivo_json):
        """Summary
        """
        self.path = path_arquivo_json
        self.dados = self.carregar()

    def carregar(self):
        """Summary
        """
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_operacoes(self):
        """Summary
        """
        return self.dados.get("operacoes", [])

    @staticmethod
    def aplicar_operacao(operacao):
        """Summary
        
        Raises:
            ValueError: Description
        """
        tipo = operacao["tipo"]

        if tipo == "identidade":
            return np.eye(3)

        elif tipo == "rotacao":
            eixo = np.array(operacao["eixo"], dtype=float)
            angulo = operacao["angulo"]
            rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
            return rot

        elif tipo == "reflexao":
            n = np.array(operacao["plano_normal"], dtype=float)
            n /= np.linalg.norm(n)
            return np.eye(3) - 2 * np.outer(n, n)

        elif tipo == "impropria":
            eixo = np.array(operacao["eixo"], dtype=float)
            angulo = operacao["angulo"]
            rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
            normal = np.array(operacao["plano_normal"], dtype=float)
            normal /= np.linalg.norm(normal)
            reflexao = np.eye(3) - 2 * np.outer(normal, normal)
            return reflexao @ rot

        else:
            raise ValueError(f"Tipo de operação desconhecido: {tipo}")