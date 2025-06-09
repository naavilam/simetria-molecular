import os, uuid
from fastapi.responses import FileResponse
from core.core_molecula import Molecule
from core.core_grupo import Group
from engine.engine_symmetry_analyser import SymmetryAnalyzer
from representation.representation_type import RepresentationType
from analysis.analise_tipo import AnaliseTipo
from render.render_tipo import RenderTipo
from main_app.main_dto import AnaliseRequest

class MoleculeSymmetryApp:
    def __init__(self, molecule, group):
        self.molecule = molecule
        self.group = group

    @classmethod
    def from_files(cls, mol_file, group_file):
        group = Group.from_file(group_file)
        molecule = Molecule.from_file(mol_file)
        return cls(molecule=molecule, group=group)

    def run(self, selected_op, config: AnaliseRequest, uuid):
        if selected_op is None:
            analises = [
                AnaliseTipo[nome.upper()]
                for nome, ativo in config.analises.items()
                if ativo
            ]
            return SymmetryAnalyzer \
                .de(self.group, self.molecule) \
                .usar(RepresentationType.PERMUTATION) \
                .configurar(analises, uuid) \
                .executar() \
                .renderizar(RenderTipo.TEX)
        else:
            return SymmetryAnalyzer \
                .de(self.group, self.molecule) \
                .usar(RepresentationType.PERMUTATION) \
                .render(RenderTipo.from_str(config.render.formato), uuid) \
                .renderizar_operacao(selected_op, paleta=config.render.paleta)


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
    return grupo

import json

import glob
import os


def encontrar_json_grupo(grupo: str) -> str:
    """
    Busca no disco o caminho do JSON correspondente ao nome do grupo.
    Exemplo: grupo = "D3h" → retorna "grupos/.../D3h.json"
    """
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
    output = app.run(selected_op=data.render.operacao_id, config=data, uuid=temp_id)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(output)
    nome_base = molecula.filename.rsplit(".", 1)[0]
    nome_tex = "Analise_Simetria_Molecula_Personalizada.tex" if nome_base.lower() in ["outro", "outro.xyz", "personalizado"] else f"Analise_Simetria_Molecula_{nome_base}.tex"
    tex_path = os.path.join(workdir, nome_tex)

    with open(tex_path, "w") as f:
        f.write(output)

    return FileResponse(tex_path, media_type="application/x-tex", filename=nome_tex)