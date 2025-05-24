import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from mpl_toolkits.mplot3d import Axes3D
from render_pyvista import visualizar_pyvista
from input_coordinates import ler_xyz
from analise_simetria import analiza_simetria

def read_input_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("xyz", help="Arquivo .xyz da molécula")
    parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria (campo 'operacoes' é lista)")
    parser.add_argument("--op", type=int, default=None, help="Índice da operação de simetria (1-based)")
    return parser.parse_args()

def load_molecule_data(xyz):
    return ler_xyz(xyz)

def load_group_symmetry_data(grupo):
    with open(grupo, "r") as f:
        return json.load(f)

def render_symmetry_op(mol, op):
    # Calcular matriz de rotação e destaque:
    Rmat, destaque = aplicar_operacao(op)
    mol_transformada = aplicar_matriz(mol, Rmat)
    print(f"Molécula transformada pela operação: {desc}")
    for elemento, coord in mol_transformada:
        x, y, z = coord
        print(f"{elemento} {x:.6f} {y:.6f} {z:.6f}")
    visualizar_pyvista(mol, mol_transformada, f"Operação: {desc}", destaque=destaque)

def select_op(operacoes, selected):
    try:
        selected_op = operacoes[selected - 1]
    except IndexError:
        print(f"Operação inválida: {selected}")
    return selected_op

def analisar_simetria(mol, group):
    analiza_simetria(mol, group)
    return

def main():

    args = read_input_arguments()
    mol = load_molecule_data(args.xyz)
    group = load_group_symmetry_data(args.grupo)
    group_op = group["operacoes"]

    if args.op is None:
        analisar_simetria(mol, group_op)
    else:
        selected_op = select_op(group_op, args.op)
        render_symmetry_op(mol, selected_op)

if __name__ == "__main__":
    main()
