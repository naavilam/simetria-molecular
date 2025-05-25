
import numpy as np
from scipy.spatial.transform import Rotation as R
from render_pyvista import visualizar_pyvista

def render_symmetry_op(mol, op):
    Rmat, destaque = detalhe_operacao(op)
    mol_transformada = aplicar_matriz(mol, Rmat)
    comentario = op["comentario"]
    desc = op.get("comentario", f"operação {comentario}")
    print(f"Molécula transformada pela operação: {desc}")
    for elemento, coord in mol_transformada:
        x, y, z = coord
        print(f"{elemento} {x:.6f} {y:.6f} {z:.6f}")
    visualizar_pyvista(mol, mol_transformada, f"Operação: {desc}", destaque=destaque)

def aplicar_matriz(molecula, Rmat):
    return [(el, Rmat @ np.array(coord)) for el, coord in molecula]

def detalhe_operacao(operacao):
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
            # "nome": operacao["nome"]
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
            # "nome": operacao["nome"]
        }

        return reflexao, destaque

    elif tipo == "impropria":
        eixo = np.array(operacao["eixo"], float)
        angulo = operacao["angulo"]
        eixo /= np.linalg.norm(eixo)
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo).as_matrix()

        # pega o normal exato do JSON
        normal = np.array(operacao["plano_normal"], float)
        normal /= np.linalg.norm(normal)

        # matriz de reflexão no plano perpendicular a esse normal
        plano = np.eye(3) - 2 * np.outer(normal, normal)

        destaque = [
            {
                "tipo":   "eixo",
                "origem": [0, 0, 0],
                "direcao": eixo.tolist(),
            },
            {
                "tipo":   "plano",
                "origem": [0, 0, 0],
                "normal": normal.tolist(),
            }
        ]

        return plano @ rot, destaque

    elif tipo == "inversao":
        centro = operacao.get("origem", [0, 0, 0])
        inversao = -np.eye(3)

        destaque = {
            "tipo": "ponto",
            "origem": centro,
            # "nome": operacao["nome"]
        }
        return inversao, destaque

    else:
        raise ValueError(f"Tipo de operação desconhecido: {tipo}")