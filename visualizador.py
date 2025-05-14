import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
from render_matplot import visualizar_matplot
from render_pyvista import visualizar_pyvista

def aplicar_matriz(molecula, Rmat):
    return [(el, Rmat @ np.array(coord)) for el, coord in molecula]
    
# def aplicar_operacao(operacao):
#     tipo = operacao["tipo"]
#     if tipo == "identidade":
#         return np.eye(3), None
#     elif tipo == "rotacao":
#         eixo = np.array(operacao["eixo"])
#         angulo = operacao["angulo"]
#         eixo = eixo / np.linalg.norm(eixo)
#         return R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix(), eixo
#     elif tipo == "reflexao":
#         n = np.array(operacao["plano_normal"])
#         n = n / np.linalg.norm(n)
#         return np.eye(3) - 2 * np.outer(n, n), n
#     elif tipo == "impropria":
#         eixo = np.array(operacao["eixo"])
#         angulo = operacao["angulo"]
#         eixo = eixo / np.linalg.norm(eixo)
#         rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()
#         plano = np.eye(3) - 2 * np.outer([0, 0, 1], [0, 0, 1])
#         return plano @ rot, eixo
#     else:
#         raise ValueError(f"Tipo de operação desconhecido: {tipo}")

def aplicar_operacao(operacao):
    tipo = operacao["tipo"]

    if tipo == "identidade":
        return np.eye(3), None

    elif tipo == "rotacao":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        eixo = eixo / np.linalg.norm(eixo)
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()

        destaque = {
            "tipo": "eixo",
            "origem": [0, 0, 0],  # ou operacao.get("origem", [0, 0, 0])
            "direcao": eixo.tolist(),
            "nome": operacao["nome"]
        }

        return rot, destaque

    elif tipo == "reflexao":
        n = np.array(operacao["plano_normal"])
        n = n / np.linalg.norm(n)
        reflexao = np.eye(3) - 2 * np.outer(n, n)

        destaque = {
            "tipo": "plano",
            "origem": [0, 0, 0],  # pode ser ajustado
            "normal": n.tolist(),
            "nome": operacao["nome"]
        }

        return reflexao, destaque

    elif tipo == "impropria":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        eixo = eixo / np.linalg.norm(eixo)
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()

        # Reflexão em plano ortogonal ao eixo
        plano = np.eye(3) - 2 * np.outer([0, 0, 1], [0, 0, 1])

        destaque = [
            {
                "tipo": "eixo",
                "origem": [0, 0, 0],
                "direcao": eixo.tolist(),
                "nome": operacao["nome"]
            },
            {
                "tipo": "plano",
                "origem": [0, 0, 0],
                "normal": [0, 0, 1],  # suposição: perpendicular ao eixo
                "nome": operacao["nome"]
            }
        ]

        return plano @ rot, destaque

    elif tipo == "inversao":
        centro = operacao.get("origem", [0, 0, 0])
        inversao = -np.eye(3)

        destaque = {
            "tipo": "ponto",
            "origem": centro,
            "nome": operacao["nome"]
        }

        return inversao, destaque

    else:
        raise ValueError(f"Tipo de operação desconhecido: {tipo}")

def ler_xyz(path):
    with open(path, 'r') as f:
        linhas = f.readlines()
    natomos = int(linhas[0])
    molecula = []
    for linha in linhas[2:2+natomos]:
        partes = linha.split()
        elemento = partes[0]
        coords = list(map(float, partes[1:4]))
        molecula.append((elemento, np.array(coords)))
    return molecula

# ... (outras funções, como aplicar_operacao, aplicar_matriz, permanecem inalteradas) 

def main():

    # Lê parâmetros de entrada:
    parser = argparse.ArgumentParser()
    parser.add_argument("xyz", help="Arquivo .xyz da molécula")
    parser.add_argument("grupo", help="Arquivo .json com o grupo de simetria (campo 'operacoes' é lista)")
    parser.add_argument("--op", type=int, default=None, help="Índice da operação de simetria (1-based)")
    parser.add_argument("--modo", choices=["matplot", "pyvista"], default=None, help="Modo de visualização (opcional)")
    args = parser.parse_args()

    mol = ler_xyz(args.xyz)

    with open(args.grupo, "r") as f:
        grupo = json.load(f)

    operacoes = grupo.get("operacoes", [])

    # Se não informar --op, listar todas as operações:
    if args.op is None:
        print("Operações disponíveis:")
        for idx, op in enumerate(operacoes, start=1):
            desc = op.get("comentario", f"operação {idx}")
            print(f"[{idx}] {desc}")
        return

    # Selecionar operação específica em parâmetro --op:
    try:
        op = operacoes[args.op - 1]
    except IndexError:
        print(f"Operação inválida: {args.op}")
        return
    desc = op.get("comentario", f"operação {args.op}")

    # Calcular matriz de rotação e destaque:
    Rmat, destaque = aplicar_operacao(op)
    mol_transformada = aplicar_matriz(mol, Rmat)

    # Se não informar --modo, imprimir coordenadas sem invocar GUI:
    if args.modo is None:
        print(f"Molécula transformada pela operação: {desc}")
        for elemento, coord in mol_transformada:
            x, y, z = coord
            print(f"{elemento} {x:.6f} {y:.6f} {z:.6f}")
        return

    # Caso contrário, invocar visualização gráfica conforme o modo escolhido:
    if args.modo == "matplot":
        visualizar_matplot(mol, mol_transformada, f"Operação: {desc}", destaque=destaque)
    elif args.modo == "pyvista":
        visualizar_pyvista(mol, mol_transformada, f"Operação: {desc}", destaque=destaque)
    else:
        # Este caso não deve ocorrer devido ao choices do argparse
        raise ValueError(f"Modo de visualização '{args.modo}' não reconhecido. Use 'matplot' ou 'pyvista'.")

if __name__ == "__main__":
    main()
