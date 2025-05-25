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
from render_pyvista import visualizar_pyvista

class OperacaoSimetria:

    """Description
    """
    
    @staticmethod
    def aplicar_matriz(molecula, Rmat):
        """Description
        
        Args:
            molecula (TYPE): Description
            Rmat (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return [(el, Rmat @ np.array(coord)) for el, coord in molecula]

    @classmethod
    def renderizar(cls, mol, op):
        """Description
        
        Args:
            mol (TYPE): Description
            op (TYPE): Description
        """
        Rmat, destaque = cls.detalhe_operacao(op)
        mol_transformada = cls.aplicar_matriz(mol, Rmat)
        comentario = op.get("comentario", op.get("nome", "operação sem nome"))
        print(f"Molécula transformada pela operação: {comentario}")
        for elemento, coord in mol_transformada:
            x, y, z = coord
            print(f"{elemento} {x:.6f} {y:.6f} {z:.6f}")
        visualizar_pyvista(mol, mol_transformada, f"Operação: {comentario}", destaque=destaque)

    @staticmethod
    def detalhe_operacao(operacao):
        """Description
        
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