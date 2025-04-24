
import plotly.graph_objects as go

def ler_xyz_para_plot(path):
    with open(path, 'r') as f:
        linhas = f.readlines()
    natomos = int(linhas[0])
    dados = []
    for linha in linhas[2:2+natomos]:
        partes = linha.split()
        elemento = partes[0]
        x, y, z = map(float, partes[1:4])
        dados.append((elemento, x, y, z))
    return dados

def visualizar_molecula(path_xyz, titulo="Visualização 3D da molécula"):
    cores = {"C": "black", "H": "lightblue"}
    raios = {"C": 0.4, "H": 0.25}

    mol = ler_xyz_para_plot(path_xyz)
    fig = go.Figure()

    for i, (el, x, y, z) in enumerate(mol):
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(size=raios.get(el, 0.3)*30, color=cores.get(el, "gray"), opacity=0.9),
            text=[f"{el}{i}"],
            textposition="top center",
            name=f"{el}{i}"
        ))

    fig.update_layout(
        title=titulo,
        scene=dict(
            xaxis=dict(title='X', backgroundcolor="white"),
            yaxis=dict(title='Y', backgroundcolor="white"),
            zaxis=dict(title='Z', backgroundcolor="white")
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    fig.show()

if __name__ == "__main__":
    visualizar_molecula("exemplos/etano_eclipsado.xyz", "Etano Eclipsado — Geometria D3h Alinhada")
