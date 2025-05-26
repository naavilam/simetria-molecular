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
from molecule import Molecule
from group_symmetry import GroupSymmetry
from molecule_symmetry import MoleculeSymmetry
from vtkmodules.vtkFiltersSources import vtkCapsuleSource

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

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


# @app.get("/api/grupo/{sistema}/{grupo}")
# async def get_grupo(sistema: str, grupo: str):
#     path = f"static/grupos/{sistema}/{grupo}.json"
#     if os.path.exists(path):
#         return FileResponse(path, media_type="application/json")
#     return {"detail": f"Grupo '{grupo}' não encontrado em '{sistema}'"}

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


class MoleculeSymmetryApp:

    """Description
    
    Attributes:
        args (TYPE): Description
        group (TYPE): Description
        group_op (TYPE): Description
        mol (TYPE): Description
    """
    
    def __init__(self):
        """Summary
        """
        self.args = self._read_input_arguments()
        self.mol = Molecule(self.args.xyz)
        self.group = GroupSymmetry(self.args.grupo)
        self.selected_op = self._validate_op(self.args.op)

    def _read_input_arguments(self):
        """Summary
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("xyz", help="Arquivo .xyz da molécula")
        parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria")
        parser.add_argument("--op", type=int, default=None, help="Índice da operação (1-based)")
        return parser.parse_args()

    def _validate_op(self, selected):
        """Valida se a operação inserida é valida
        """
        if self.args.op is None:
            self.selected_op = None
            return
        else:
            try:
                self.selected_op = self.args.op
                return self.group.get_operacoes()[selected - 1]
            except IndexError:
                print(f"Operação inválida: {selected}")
                return None

    def _run(self):
        """Caso tenha escolhido a operação esta é renderizada, 
        caso contrário é feita uma análise completa da simetria
        """
        ms = MoleculeSymmetry(self.mol, self.group)
        
        if self.selected_op is None:
            ms.analize_symmetry()
        else:
            ms.render_symmetry_operation(self.selected_op)


#####################################################################################
#Backend Hugging face

# import gradio as gr

# # ========================================
# # 🔹 Interface gráfica (Gradio)
# # ========================================

# def launch_interface():
#     interface = gr.Interface(
#         fn=render,
#         inputs=[
#             gr.Textbox(label="Molécula (.xyz)", lines=10),
#             gr.Textbox(label="Grupo de simetria (.json)", lines=10),
#             gr.Number(label="Operação #", value=1)
#         ],
#         outputs=gr.HTML(label="Visualização 3D")
#     )
#     interface.launch()


# # ========================================
# # 🔹 Função usada pela interface Gradio
# # ========================================
# def render(mol_xyz, grupo_json, operacao_id):
#     try:
#         linhas = mol_xyz.strip().splitlines()
#         coords = [list(map(float, linha.split()[1:4])) for linha in linhas[2:]]
#         coords = np.array(coords)

#         grupo = json.loads(grupo_json)
#         op = grupo["operacoes"][int(operacao_id) - 1]
#         eixo = np.array(op["eixo"])
#         angulo = np.deg2rad(op["angulo"])
#         rot = pv.transformations.axis_angle_rotation_matrix(eixo, angulo)

#         coords_rot = coords @ rot.T
#         p = pv.Plotter(off_screen=True)
#         p.add_points(coords, color="gray")
#         p.add_points(coords_rot, color="blue")
#         html_path = "/tmp/render.html"
#         p.export_html(html_path)
#         return html_path
#     except Exception as e:
#         return f"<pre>{str(e)}</pre>"

# ========================================
# 🔹 Fim Gradio
# ========================================
# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         app = MoleculeSymmetryApp()
#         app._run()
#     else:
#         launch_interface() # 🌐 Modo Gradio











