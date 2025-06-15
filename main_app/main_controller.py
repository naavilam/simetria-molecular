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

from fastapi import UploadFile
from fastapi.responses import FileResponse
import os
import uuid
from model.model_molecula import Molecule
from main_app.main_dto import AnaliseRequest
from engine_analyzer.molecule_symmetry_app import MoleculeSymmetryApp
from render.render_tipo import RenderTipo

async def processar_analise(molecula: UploadFile, data: AnaliseRequest):
    """Processa a análise de simetria molecular, gera e entrega o resultado no formato desejado.
    """

    temp_id = gerar_uuid_temporario()
    workdir = criar_diretorio_temporario(temp_id)
    mol_str = await ler_molecula_uploadfile(molecula)

    app = (
        MoleculeSymmetryApp(mol_str)
        .config(data.analises)
        .config(data.render)
        .config(temp_id)
    )

    output = app.run()

    return salvar_e_retornar_saida(output, workdir, temp_id, data.render.formato)

def gerar_uuid_temporario() -> str:
    return f"SIM{uuid.uuid4().hex[:6].upper()}"

def criar_diretorio_temporario(temp_id: str) -> str:
    workdir = f"/tmp/analise_{temp_id}"
    os.makedirs(workdir, exist_ok=True)
    return workdir

async def ler_molecula_uploadfile(molecula) -> str:
    return (await molecula.read()).decode('utf-8')

def salvar_e_retornar_saida(output, workdir, temp_id, formato: RenderTipo):
    if formato == RenderTipo.TEX:
        return salvar_arquivo_texto(output, workdir, temp_id, ".tex", "application/x-tex")

    elif formato == RenderTipo.PDF:
        return salvar_arquivo_binario(output, workdir, temp_id, ".pdf", "application/pdf")

    elif formato in [RenderTipo.D3, RenderTipo.GIF]:
        return PlainTextResponse(output)

    else:
        return PlainTextResponse(f"[ERRO] Formato de saída desconhecido: {formato}")

def salvar_arquivo_texto(output: str, workdir: str, temp_id: str, extensao: str, media_type: str):
    nome_saida = f"{temp_id}{extensao}"
    saida_path = os.path.join(workdir, nome_saida)
    with open(saida_path, "w") as f:
        f.write(output)
    return FileResponse(saida_path, media_type=media_type, filename=nome_saida)

def salvar_arquivo_binario(output: bytes, workdir: str, temp_id: str, extensao: str, media_type: str):
    nome_saida = f"{temp_id}{extensao}"
    saida_path = os.path.join(workdir, nome_saida)
    with open(saida_path, "wb") as f:
        f.write(output)
    return FileResponse(saida_path, media_type=media_type, filename=nome_saida)