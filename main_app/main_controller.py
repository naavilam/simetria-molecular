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

import os, uuid
import glob
import os
from fastapi.responses import FileResponse
from model.model_molecula import Molecule
from model.model_grupo import Group
from engine.engine_symmetry_analyser import SymmetryAnalyzer
from representation.representation_type import RepresentationType
from analysis.analise_tipo import AnaliseTipo
from render.render_tipo import RenderTipo
from main_app.main_dto import AnaliseRequest
from main_app.app_symmetry import MoleculeSymmetryApp
from pymatgen.core.structure import Molecule as PymatgenMolecule
from pymatgen.symmetry.analyzer import PointGroupAnalyzer

def identificar_grupo_pontual(xyz_path: str) -> str:
    with open(xyz_path) as f:
        lines = f.readlines()[2:]
        especies = []
        coords = []
        for line in lines:
            tokens = line.strip().split()
            especies.append(tokens[0])
            coords.append([float(x) for x in tokens[1:4]])
    mol = PymatgenMolecule(especies, coords)
    grupo = PointGroupAnalyzer(mol).sch_symbol  # Ex: "D3h"
    print(">>> Grupo identificado:")
    print(grupo)
    return grupo

def encontrar_json_grupo(grupo: str) -> str:
    grupo_proc = grupo.strip().lower()
    arquivos = glob.glob("static/grupos/**/*.json", recursive=True)

    for path in arquivos:
        nome_arquivo = os.path.splitext(os.path.basename(path))[0].lower()
        if nome_arquivo == grupo_proc or nome_arquivo.startswith(grupo_proc):
            return path

    raise FileNotFoundError(f"Arquivo JSON para o grupo '{grupo}' não encontrado.")

async def processar_analise(molecula, data: AnaliseRequest):
    temp_id = f"SIM{uuid.uuid4().hex[:6].upper()}"  # SIM_97DC9F
    workdir = f"/tmp/analise_{temp_id}"
    os.makedirs(workdir, exist_ok=True)

    mol_path = os.path.join(workdir, molecula.filename)

    with open(mol_path, "wb") as f:
        f.write(await molecula.read())

    grupo_identificado = identificar_grupo_pontual(mol_path)
    grupo_path = encontrar_json_grupo(grupo_identificado)

    app = MoleculeSymmetryApp.from_files(mol_path, grupo_path)
    output = app.run(render=data.render, analises=data.analises, uuid=temp_id)

    nome_base = molecula.filename.rsplit(".", 1)[0]
    nome_tex = "Analise_Simetria_Molecula_Personalizada.tex" if nome_base.lower() in ["outro", "outro.xyz", "personalizado"] else f"Analise_Simetria_Molecula_{nome_base}.tex"
    tex_path = os.path.join(workdir, nome_tex)

    with open(tex_path, "w") as f:
        f.write(output)

    return FileResponse(tex_path, media_type="application/x-tex", filename=nome_tex)





