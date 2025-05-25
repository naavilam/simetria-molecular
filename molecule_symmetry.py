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

import numpy as np
from group_symmetry import GroupSymmetry
from tabela_multiplicacao import TabelaMultiplicacao
from classe_conjugacao import ClasseConjugacao
from scipy.spatial.transform import Rotation as R
from render_pyvista import visualizar_pyvista
from molecule import Molecule


class MoleculeSymmetry:

    """Description
    
    Attributes:
        mol (TYPE): Description
        operacoes (TYPE): Description
        permutacoes (dict): Description
    """
    
    def __init__(self, molecule, group):
        self.molecule = molecule
        self.group = group

    def analize_symmetry(self):
        """Executa a análise de simetria e imprime os resultados.
        """
        print("Operações de simetria disponíveis:")
        permutacoes = {}
        for idx, op in enumerate(self.group.get_operacoes(), start=1):
            desc = op.get("comentario", f"operação {idx}")
            print(f"[{idx}] {desc}")
            Rmat, destaque = self.group.detalhe_operacao(op)
            mol_transformada = self._aplicar_matriz(Rmat)
            permutacao = self._obter_permutacao(self.molecule, mol_transformada)
            permutacoes[op["nome"]] = permutacao

        print("*****************Permutações Básicas*****************")
        self._list_permutations(permutacoes)
        print("********Fim da Analise das Permutações Básicas*******")


        tab_mult = TabelaMultiplicacao(permutacoes).gerar()
        class_conj = ClasseConjugacao(permutacoes, tab_mult).gerar_classe_conjugacao()

    def render_symmetry_operation(self, operation):
        """Calcula apenas a operacao selecionada e renderiza imagem da molecula 
        antes e depois em modo 3D interativo
        
        Args:
            operation (TYPE): Description
        """
        Rmat, destaque = GroupSymmetry.detalhe_operacao(operation)
        mol_transformada = self._aplicar_matriz(Rmat)
        comentario = operation.get("comentario", operation.get("nome", "operação sem nome"))
        print(f"Molécula transformada pela operação: {comentario}")
        for elemento, coord in mol_transformada.como_tuplas():
            x, y, z = coord
            print(f"{elemento} {x:.6f} {y:.6f} {z:.6f}")
        visualizar_pyvista(self.molecule, mol_transformada, f"Operação: {comentario}", destaque=destaque)


    def _obter_permutacao(self, orig_coords, transf_coords, tol=1e-3):
        """Compara coordenadas para identificar a permutação resultante.
        
        Args:
            orig_coords (list): Lista de coordenadas originais.
            transf_coords (list): Lista de coordenadas transformadas.
            tol (float): Tolerância para comparacão de similaridade.
        
        Returns:
            list: Permutação dos índices.
        """
        permutacao = []
        for _, coord in transf_coords:
            for i, (_, ref) in enumerate(orig_coords.como_tuplas()):
                if np.allclose(coord, ref, atol=tol):
                    permutacao.append(i)
                    break
            else:
                permutacao.append(None)
        return permutacao

    def _aplicar_matriz(self, Rmat):
        """Description
        
        Args:
            molecula (TYPE): Description
            Rmat (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        elementos = [el for el, _ in self.molecule.como_tuplas()]
        coords = [Rmat @ np.array(coord) for _, coord in self.molecule.como_tuplas()]
        nova = Molecule.__new__(Molecule)
        nova.elementos = elementos
        nova.coordenadas = coords
        return nova
        # return [(el, Rmat @ np.array(coord)) for el, coord in self.molecule.como_tuplas()]


    def _aplicar_operacao(self, operacao):
        """Summary
        
        Raises:
            ValueError: Description
        """
        tipo = operacao["tipo"]

        if tipo == "identidade":
            return np.eye(3)

        elif tipo == "rotacao":
            eixo = np.array(operacao["eixo"], dtype=float)
            angulo = operacao["angulo"]
            rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
            return rot

        elif tipo == "reflexao":
            n = np.array(operacao["plano_normal"], dtype=float)
            n /= np.linalg.norm(n)
            return np.eye(3) - 2 * np.outer(n, n)

        elif tipo == "impropria":
            eixo = np.array(operacao["eixo"], dtype=float)
            angulo = operacao["angulo"]
            rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
            normal = np.array(operacao["plano_normal"], dtype=float)
            normal /= np.linalg.norm(normal)
            reflexao = np.eye(3) - 2 * np.outer(normal, normal)
            return reflexao @ rot

        else:
            raise ValueError(f"Tipo de operação desconhecido: {tipo}")

    def _list_permutations(self, permutacoes):
        for nome, perm in permutacoes.items():
            print(f"{nome}: {perm}")