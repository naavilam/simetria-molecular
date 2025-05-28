from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from .main_controller import processar_analise
from .main_dto import AnaliseRequest

import os, uuid

router = APIRouter()

@router.get("/api/grupo/{familia}/{geometria}/{grupo}")
def get_grupo_cristalografico(familia: str, geometria: str, grupo: str):
    path = f"static/grupos/{familia}/{geometria}/{grupo}.json"
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return {"detail": f"Grupo '{grupo}.json' não encontrado em '{geometria}'"}

@router.get("/api/grupo/{familia}/{grupo}")
def get_grupo_molecular(familia: str, grupo: str):
    path = f"static/grupos/{familia}/{grupo}.json"
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return {"detail": f"Grupo '{grupo}.json' não encontrado em '{familia}'"}

@router.get("/api/molecula/{nome}")
async def get_molecula(nome: str):
    path = f"static/moleculas/{nome}.xyz"
    if os.path.exists(path):
        return FileResponse(path, media_type="text/plain")
    return {"detail": f"Molécula '{nome}' não encontrada"}

@router.post("/api/analise")
async def analise(molecula: UploadFile = File(...), grupo: UploadFile = File(...), payload: str = Form(...)):
    data = AnaliseRequest.parse_raw(payload)
    return await processar_analise(molecula, grupo, data)