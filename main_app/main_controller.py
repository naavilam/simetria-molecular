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

    def run(self, selected_op, config: AnaliseRequest):
        if selected_op is None:
            analises = [
                AnaliseTipo[nome.upper()]
                for nome, ativo in config.analises.items()
                if ativo
            ]

            return SymmetryAnalyzer \
                .de(self.group, self.molecule) \
                .usar(RepresentationType.PERMUTATION) \
                .render(RenderTipo(config.render.formato.upper())) \
                .configurar(analises=analises) \
                .get()

        else:
            return SymmetryAnalyzer \
                .de(self.group, self.molecule) \
                .usar(RepresentationType.PERMUTATION) \
                .render(RenderTipo(config.render.formato.upper())) \
                .renderizar_operacao(selected_op, paleta=config.render.paleta)


async def processar_analise(molecula, grupo, data: AnaliseRequest):
    temp_id = str(uuid.uuid4())
    workdir = f"/tmp/analise_{temp_id}"
    os.makedirs(workdir, exist_ok=True)

    mol_path = os.path.join(workdir, molecula.filename)
    grupo_path = os.path.join(workdir, grupo.filename)

    with open(mol_path, "wb") as f:
        f.write(await molecula.read())
    with open(grupo_path, "wb") as f:
        f.write(await grupo.read())

    app = MoleculeSymmetryApp.from_files(mol_path, grupo_path)
    output = app.run(selected_op=data.render.operacao_id, config=data)

    nome_base = molecula.filename.rsplit(".", 1)[0]
    nome_tex = "Analise_Simetria_Molecula_Personalizada.tex" if nome_base.lower() in ["outro", "outro.xyz", "personalizado"] else f"Analise_Simetria_Molecula_{nome_base}.tex"
    tex_path = os.path.join(workdir, nome_tex)

    with open(tex_path, "w") as f:
        f.write(output)

    return FileResponse(tex_path, media_type="application/x-tex", filename=nome_tex)