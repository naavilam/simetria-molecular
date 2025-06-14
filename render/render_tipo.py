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

from enum import Enum, auto

class RenderTipo(Enum):
    D3 = auto()
    GIF = auto()
    TEX = auto()
    PDF = auto()

    @classmethod
    def from_str(cls, valor: str) -> 'RenderTipo':
        mapa = {
            "3d": cls.D3,
            "gif": cls.GIF,
            "tex": cls.TEX,
            "pdf": cls.PDF,
        }
        try:
            return mapa[valor.lower()]
        except KeyError:
            raise ValueError(f"Tipo de renderização inválido: {valor}")
