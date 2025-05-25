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

import argparse
from load_molecules import ler_xyz
from load_groups import load_group_symmetry_data
from analise_simetria import analiza_simetria
from gera_permutacoes import render_symmetry_op

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
        self.mol = ler_xyz(self.args.xyz)
        self.group = load_group_symmetry_data(self.args.grupo)
        self.group_op = self.group["operacoes"]

    def _read_input_arguments(self):
        """Summary
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("xyz", help="Arquivo .xyz da molécula")
        parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria")
        parser.add_argument("--op", type=int, default=None, help="Índice da operação (1-based)")
        return parser.parse_args()

    def _validate_op(self, selected):
        """Summary
        """
        try:
            return self.group_op[selected - 1]
        except IndexError:
            print(f"Operação inválida: {selected}")
            return None

    def _run(self):
        """Summary
        """
        if self.args.op is None:
            analiza_simetria(self.mol, self.group_op)
        else:
            selected_op = self._validate_op(self.args.op)
            if selected_op:
                render_symmetry_op(self.mol, selected_op)

if __name__ == "__main__":
    app = MoleculeSymmetryApp()
    app._run()