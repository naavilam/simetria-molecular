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

from enum import Enum

class AnaliseTipo(Enum):

    """Summary
    """

    PERMUTACOES = "permutacoes"
    TABELA_MULTIPLICACAO = "tabela_multiplicacao"
    CLASSES_CONJUGACAO = "classes_conjugacao"
    SUB_GRUPOS = "sub_grupos"
    AUTO_VALORES = "auto_valores"
    ABELIANO = "abeliano"
    CICLICO = "ciclico"
    TABELA_CARACTERES = "tabela_caracteres"
    GRUPO = "grupo"

    @classmethod
    def from_str(cls, valor: str) -> 'AnaliseTipo':
        mapa = {item.value.lower(): item for item in cls}
        try:
            return mapa[valor.lower()]
        except KeyError:
            raise ValueError(f"Tipo de análise inválido: '{valor}'. Opções válidas: {list(mapa.keys())}")