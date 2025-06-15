"""=================================================================================================================================================
**                                                   Copyright © 2025 Chanah Yocheved Bat Sarah                                                   **
**                                                                                                                                                **
**                                                       Author: Chanah Yocheved Bat Sarah                                                        **
**                                                          Contact: contact@chanah.dev                                                           **
**                                                                Date: 2025-06-15                                                                **
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

from analysis.analise import Analise
from model.model_molecula import Molecule
from model.model_operacao_simetria import SymmetryOperation
from pymatgen.symmetry.analyzer import PointGroupAnalyzer
from pymatgen.core.structure import Molecule as PymatgenMolecule
import glob
import os
# Placeholder temporário até implementarmos o cálculo na unha
from utils.grupo_identificacao import identificar_grupo_pontual, encontrar_json_grupo  # Ajuste seu import conforme seu projeto

class AnaliseGrupo(Analise):
    def __init__(self, molecule: Molecule):
        self.molecule = molecule
        self._resultado = {}

    def executar(self) -> dict:
        grupo_nome = self.identificar_grupo_pontual(molecule)
        grupo_path = self.encontrar_json_grupo(grupo_nome)
        operacoes = self.carregar_operacoes(grupo_path)
        sistema = self.determinar_sistema(grupo_path)

        self._resultado = {
            "nome": grupo_nome,
            "ordem": len(operacoes),
            "sistema": sistema,
            "operacoes": [op.to_dict() for op in operacoes]
        }

        return self._resultado

    def identificar_grupo_pontual(self, molecule: Molecule) -> str:
        especies = [atom.elemento for atom in molecule.elemento]
        coords = [atom.coordenadas for atom in molecule.elemento]
        mol = PymatgenMolecule(especies, coords)
        return PointGroupAnalyzer(mol).sch_symbol

    def encontrar_json_grupo(self, grupo_nome: str) -> str:
        grupo_proc = grupo_nome.strip().lower()
        arquivos = glob.glob("static/grupos/**/*.json", recursive=True)
        for path in arquivos:
            nome_arquivo = os.path.splitext(os.path.basename(path))[0].lower()
            if nome_arquivo == grupo_proc or nome_arquivo.startswith(grupo_proc):
                return path
        raise FileNotFoundError(f"Arquivo JSON para grupo '{grupo_nome}' não encontrado.")

    def carregar_operacoes(self, grupo_path: str) -> List[SymmetryOperation]:
        with open(grupo_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        operacoes = []
        for idx, operacao_data in enumerate(data.get("operacoes", []), start=1):
            op = SymmetryOperation(
                id=idx,
                tipo=operacao_data.get("tipo"),
                eixo=operacao_data.get("eixo"),
                angulo=operacao_data.get("angulo"),
                plano_normal=operacao_data.get("plano_normal"),
                comentario=operacao_data.get("comentario"),
                nome=operacao_data.get("nome")
            )
            operacoes.append(op)

        return operacoes

    def determinar_sistema(self, grupo_path: str) -> str:
        grupo_path_norm = os.path.normpath(grupo_path)
        partes = grupo_path_norm.split(os.sep)
        for i, parte in enumerate(partes):
            if parte.lower() == "cristalograficos" and i + 1 < len(partes):
                return partes[i + 1]
        return "Desconhecido"