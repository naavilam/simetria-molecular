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

from render.render_tipo import RenderTipo
from pydantic import BaseModel, field_validator
from typing import Optional, Dict
from analysis.analise_tipo import AnaliseTipo

class RenderConfig(BaseModel):
    formato: RenderTipo
    paleta: Optional[str] = None

    @field_validator('formato', mode='before')
    @classmethod
    def parse_formato(cls, v):
        if isinstance(v, str):
            return RenderTipo.from_str(v)
        return v

class AnaliseRequest(BaseModel):

    """Summary
    """

    render: RenderConfig
    analises: Dict[str, bool]

    @field_validator('analises', mode='before')
    @classmethod
    def parse_analises(cls, value):
        resultado = {}
        for nome, ativo in value.items():
            try:
                tipo = AnaliseTipo.from_str(nome)
                resultado[tipo] = ativo
            except ValueError:
                raise ValueError(f"Tipo de análise inválido: {nome}")
        return resultado