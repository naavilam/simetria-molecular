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

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional
from fastapi import UploadFile, File, Form
from .main_controller import processar_analise
from .main_dto import AnaliseRequest
from analysis.analise_tipo import AnaliseTipo

import os, uuid

router = APIRouter()

@router.get("/api/molecula/{nome}")
async def get_molecula(nome: str):
    path = f"static/moleculas/{nome}.xyz"
    if os.path.exists(path):
        return FileResponse(path, media_type="text/plain")
    return {"detail": f"Molécula '{nome}' não encontrada"}

@router.post("/api/analise")
async def analise(
    molecula: UploadFile = File(...),
    payload: Optional[str] = Form(None)
):   
    data = AnaliseRequest.parse_raw(payload)
    return await processar_analise(molecula, data)

@router.get("/api/analises/")
async def get_analises():
    return AnaliseTipo.__getattribute__

