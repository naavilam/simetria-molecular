
import numpy as np
from scipy.spatial.transform import Rotation as R
import json

# def carregar_grupo_json(path_json):
#     with open(path_json, 'r') as f:
#         dados = json.load(f)
#     return dados["operacoes"]

def load_group_symmetry_data(grupo):
    with open(grupo, "r") as f:
        return json.load(f)
        
def aplicar_operacao(operacao):
    tipo = operacao["tipo"]

    if tipo == "identidade":
        return np.eye(3)

    elif tipo == "rotacao":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
        return rot

    elif tipo == "reflexao":
        n = np.array(operacao["plano_normal"])
        n = n / np.linalg.norm(n)
        return np.eye(3) - 2 * np.outer(n, n)

    elif tipo == "impropria":
        eixo = np.array(operacao["eixo"])
        angulo = operacao["angulo"]
        rot = R.from_rotvec(np.deg2rad(angulo) * eixo / np.linalg.norm(eixo)).as_matrix()
        normal = eixo / np.linalg.norm(eixo)
        reflexao = np.eye(3) - 2 * np.outer(normal, normal)
        return reflexao @ rot

    else:
        raise ValueError(f"Tipo de operação desconhecido: {tipo}")
