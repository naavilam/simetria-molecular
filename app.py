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

import sys
import argparse

from numpy import select
from core.molecule import Molecule
from core.group import Group
from engine.symmetry_analyser import SymmetryAnalyser
from engine.symmetry_visualizer import SymmetryVisualizer
from vtkmodules.vtkFiltersSources import vtkCapsuleSource
from core.operation import Operation
from representation_strategy_builder import RepresentationType

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os, shutil, zipfile, uuid, json
from analise.analise_tipo import AnaliseTipo
from render.render_tipo import RenderTipo

# Ativa modo FastAPI
app = FastAPI()

# Libera CORS para todos os domínios (inclusive seu GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua por ['https://naavilam.github.io'] se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para expor arquivos JSON dos grupos
@app.get("/api/grupo/{familia}/{geometria}/{grupo}")
def get_grupo_cristalografico(familia: str, geometria: str, grupo: str):
    path = f"static/grupos/{familia}/{geometria}/{grupo}.json"
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return {"detail": f"Grupo '{grupo}.json' não encontrado em '{geometria}'"}

@app.get("/api/grupo/{familia}/{grupo}")
def get_grupo_molecular(familia: str, grupo: str):
    path = f"static/grupos/{familia}/{grupo}.json"
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return {"detail": f"Grupo '{grupo}.json' não encontrado em '{familia}'"}

# Endpoint para expor arquivos JSON das moléculas
@app.get("/api/molecula/{nome}")
async def get_molecula(nome: str):
    path = f"static/moleculas/{nome}.xyz"
    if os.path.exists(path):
        return FileResponse(path, media_type="text/plain")
    return {"detail": f"Molécula '{nome}' não encontrada"}

@app.post("/api/analise")
async def analise(
    molecula: UploadFile = File(...),
    grupo: UploadFile = File(...)
):
    # Criar pasta temporária única
    temp_id = str(uuid.uuid4())
    workdir = f"/tmp/analise_{temp_id}"
    os.makedirs(workdir, exist_ok=True)

    # Salvar arquivos
    mol_path = os.path.join(workdir, molecula.filename)
    grupo_path = os.path.join(workdir, grupo.filename)

    with open(mol_path, "wb") as f:
        f.write(await molecula.read())
    with open(grupo_path, "wb") as f:
        f.write(await grupo.read())

    conteudo_latex = MoleculeSymmetryApp.from_files(mol_path, grupo_path).run(selected_op=None)
    
    # Nomeia arquivo latex de resposta
    nome_base = molecula.filename.rsplit(".", 1)[0]
    if nome_base.lower() in ["outro", "outro.xyz", "personalizado"]:
        nome_tex = "Analise_Simetria_Molecula_Personalizada.tex"
    else:
        nome_tex = f"Analise_Simetria_Molecula_{nome_base}.tex"

    # Caminho completo
    tex_path = os.path.join(workdir, nome_tex)

    with open(tex_path, "w") as f:
        f.write(conteudo_latex)

    return FileResponse(tex_path, media_type="application/x-tex", filename=nome_tex)

# @app.post("/api/renderizar")
# async def renderizar(
#     selected_op: op
# ):
#     # Criar pasta temporária única
#     temp_id = str(uuid.uuid4())
#     workdir = f"/tmp/analise_{temp_id}"
#     os.makedirs(workdir, exist_ok=True)

#     # Salvar arquivos
#     mol_path = os.path.join(workdir, molecula.filename)
#     grupo_path = os.path.join(workdir, grupo.filename)

#     with open(mol_path, "wb") as f:
#         f.write(await molecula.read())
#     with open(grupo_path, "wb") as f:
#         f.write(await grupo.read())

#     app = MoleculeSymmetryApp.from_files(molecula, grupo).run(selected_op)

class MoleculeSymmetryApp:

    """Description
    
    Attributes:
        args (TYPE): Description
        group (TYPE): Description
        group_op (TYPE): Description
        mol (TYPE): Description
    """
    
    def __init__(self, molecule, group):
        """Summary
        """
        self.molecule = molecule
        self.group = group

    @classmethod
    def from_files(cls, mol_file, group_file):
        group = Group.from_file(group_file)
        molecule = Molecule.from_file(mol_file)
        return cls(molecule=molecule, group=group)

    def _get_op(self, selected, group):
        """Valida se a operação inserida é valida
        """
        try:
            return group.operacoes[selected - 1]
        except IndexError:
            print(f"Operação inválida: {selected}")
            return None

    def run(self, selected_op):
        """Caso tenha escolhido a operação esta é renderizada, 
        caso contrário é feita uma análise completa da simetria
        """

        analises_selecionadas = [AnaliseTipo.TABELA_MULTIPLICACAO, AnaliseTipo.ABELIANO]


        if selected_op is None:
            symmetry_analysis = SymmetryAnalyzer \
                .de(self.grupo, self.molecule) \
                .usar(RepresentationType.PERMUTATION) \
                .render(RenderTipo.LATEX)
                .configurar(analises=analises_selecionadas)
                .get()

            return symmetry_analysis
        else:


        # sym_analyzer = SymmetryAnalyser(self.mol, self.group)

        # if selected_op is None:
        #     return sym_analyzer.run_analysis()
        # else:
        #     selected_op = self._get_op(selected_op, self.group)
        #     sym_visualizer = SymmetryVisualizer(self.mol, )
        #     return sym_visualizer.render(selected_op)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xyz", help="Arquivo .xyz da molécula")
    parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria")
    parser.add_argument("--op", type=int, default=None, help="Índice da operação (1-based)")
  
    args = parser.parse_args()
    xyz = args.xyz
    grupo = args.grupo
    op = args.op

    app = MoleculeSymmetryApp.from_files(xyz, grupo)
    
    # Apenas para os testes de formatação latex esta sendo exibido no terminal
    # if op is not None :
    #     app.run(op)
    # else:
    #     conteudo_latex = app.run(op)
    #     # Mostrar no terminal
    #     print(conteudo_latex)

    #     # Opcional: salvar localmente para inspeção
    #     with open("analise_terminal.tex", "w") as f:
    #         f.write(conteudo_latex)

    #     print("Arquivo 'analise_terminal.tex' gerado com sucesso!")

