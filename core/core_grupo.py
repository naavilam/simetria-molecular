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

from enum import nonmember
import numpy as np
from scipy.spatial.transform import Rotation as R
# from core.operation import Operation
import json

class Group:

    """Summary
    """
    def __init__(self, sistema, nome, ordem, operacoes, tolerancia):
        """Summary
        """
        self.sistema = sistema
        self.nome = nome
        self.operacoes = operacoes
        self.ordem = ordem
        self.tolerancia = tolerancia

    @classmethod
    def from_file(cls, path_json):
        return cls._carregar(path_json)

    @classmethod
    def _carregar(cls, path_json):
        """Carrega grupo de simetria a partir de arquivo JSON, inferindo o sistema pelo caminho."""
        import os

        with open(path_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        nome = dados.get("nome")
        ordem = dados.get("ordem")
        operacoes = dados.get("operacoes")
        tolerancia = dados.get("tolerancia")

        # Tentar inferir sistema a partir do caminho
        caminho = os.path.normpath(path_json)
        partes = caminho.split(os.sep)

        sistema = "Molecular"  # valor padrão se não for identificado
        if "grupos" in partes:
            try:
                idx_grupo = partes.index("grupos")
                # sistema_parts = partes[idx_grupo + 1:-1]  # subpastas após 'grupo' e antes do arquivo
                sistema_parts = partes[idx_grupo + 1:]
                if sistema_parts and sistema_parts[-1].endswith(".json"):
                    sistema_parts = sistema_parts[:-1]
                sistema_corrigido = []

                for p in sistema_parts:
                    if p.lower() == "cristalograficos":
                        sistema_corrigido.append("Cristalográfico")
                    else:
                        sistema_corrigido.append(p.capitalize())

                if sistema_corrigido:
                    sistema = " ".join(sistema_corrigido)

            except Exception:
                pass  # mantemos sistema = "Molecular"

        return cls(sistema, nome, ordem, operacoes, tolerancia)

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
