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
    """Summary

    Raises:
        FileNotFoundError: Description
    """
    grupo_proc = grupo.strip().lower()
    arquivos = glob.glob("static/grupos/**/*.json", recursive=True)

    for path in arquivos:
        nome_arquivo = os.path.splitext(os.path.basename(path))[0].lower()
        if nome_arquivo == grupo_proc or nome_arquivo.startswith(grupo_proc):
            return path

    raise FileNotFoundError(f"Arquivo JSON para o grupo '{grupo}' não encontrado.")


grupo_identificado = identificar_grupo_pontual(mol_path)
grupo_path = encontrar_json_grupo(grupo_identificado)