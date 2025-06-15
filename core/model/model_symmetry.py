"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-06-14                                                                **
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

from typing import List
from fastapi.openapi.models import Components
import numpy as np
from typing import List, Optional

class SymmetryOperation:
    """
    Blueprint abstrato de uma operação de simetria.

    Essa classe descreve a essência conceitual da operação (tipo, eixo, ângulo, plano, etc),
    mas NÃO contém nenhuma representação matemática (matriz, permutação, etc).
    """

    def __init__(
        self,
        tipo: str,
        nome: Optional[str] = None,
        id: Optional[int] = None,
        eixo: Optional[List[float]] = None,
        angulo: Optional[float] = None,
        plano_normal: Optional[List[float]] = None,
        comentario: Optional[str] = None
    ):
        """
        Args:
            tipo (str): Tipo da operação (ex: 'identidade', 'rotacao', 'reflexao', 'inversao', etc)
            nome (str, opcional): Nome simbólico (ex: "mathrm{C}_3", "sigma_h", etc)
            id (int, opcional): ID da operação dentro do grupo
            eixo (List[float], opcional): Eixo da operação, se aplicável
            angulo (float, opcional): Ângulo de rotação (em graus), se aplicável
            plano_normal (List[float], opcional): Normal do plano de reflexão, se aplicável
        """
        self.tipo = tipo
        self.nome = nome
        self.id = id
        self.eixo = eixo
        self.angulo = angulo
        self.plano_normal = plano_normal
        self.comentario = comentario

    def __repr__(self):
        return f"SymmetryOperation(id={self.id}, tipo='{self.tipo}', nome='{self.nome}')"

    def as_dict(self) -> dict:
        """
        Exporta a operação para um dicionário (útil para JSON ou logs).

        Returns:
            dict: Representação em dicionário.
        """
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nome": self.nome,
            "eixo": self.eixo,
            "angulo": self.angulo,
            "plano_normal": self.plano_normal,
            "comentario": self.comentario
        }
