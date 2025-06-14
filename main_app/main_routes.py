from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional
from fastapi import UploadFile, File, Form
from .main_controller import processar_analise
from .main_dto import AnaliseRequest

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
    print("Formato escolhido:", data.render.formato)
    print("Paleta (se houver):", data.render.paleta)
    print("Análises escolhidas:", data.analises)
    return await processar_analise(molecula, data)



