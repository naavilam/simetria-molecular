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

from typing import overload, Union
from model.model_molecula import Molecule
from engine.engine_symmetry_analyser import SymmetryAnalyzer
from analysis.analise_tipo import AnaliseTipo
from render.builder import RendererBuilder
from engine_analyser.symmetry_analyzer import SymmetryAnalyzer
from main_app.main_dto import RenderConfig

class MoleculeSymmetryApp:
    """Main application for molecular symmetry analysis.
    """

    def __init__(self, molecule: str):
        self.molecule = Molecule.from_data(molecule)
        self.analyser = SymmetryAnalyzer(self.molecule)
        self.renderer = None
        self._uuid = None

    def config(self, param: Union[list, RenderConfig, str]) -> 'MoleculeSymmetryApp':
        """Summary

        Raises:
            TypeError: Description
        """
        if isinstance(param, list):
            self.analyser.set(param)

        elif isinstance(param, RenderConfig):
            self.renderer = RendererBuilder.getRenderer(param)

        elif isinstance(param, str):
            self._uuid = param

        else:
            raise TypeError(f"Tipo de configuração inválido: {type(param)}")

        return self

    def run(self) -> str:
        """Executa as análises e realiza o render final."""

        # 1. Executa as análises de acordo com a estratégia
        results = self.analyser.execute()

        # 2. Gera os metadados
        metadata = self.analyser.generate_metadata(self._uuid)

        # 3. Passa os metadados para o renderer
        self.renderer.set_metadata(metadata)

        # 4. Renderiza o resultado
        return self.renderer.render(results)

